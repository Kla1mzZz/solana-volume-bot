import base58
import asyncio
import time

from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solders.transaction import VersionedTransaction
from solders.system_program import TransferParams, transfer
from solders.message import MessageV0
from solana.exceptions import SolanaRpcException
from solana.rpc.core import RPCException
from spl.token.instructions import get_associated_token_address

from database import get_wallets, get_main_wallet, get_token_address
from service.transaction_service import sell_token
from utils.styles import console


client = AsyncClient('https://solana-rpc.publicnode.com')


class BlockhashCache:
    def __init__(self, client, ttl=15):
        self.client = client
        self.ttl = ttl
        self.blockhash = None
        self.timestamp = 0

    async def get_blockhash(self, retries=5, delay=3):
        now = time.time()
        if not self.blockhash or now - self.timestamp > self.ttl:
            for attempt in range(retries):
                try:
                    resp = await self.client.get_latest_blockhash()
                    self.blockhash = resp.value.blockhash
                    self.timestamp = now
                    return self.blockhash
                except SolanaRpcException as e:
                    if '429' in str(e) or 'Too Many Requests' in str(e):
                        print(
                            f'Rate limit hit getting blockhash, waiting {delay}s (attempt {attempt + 1})'
                        )
                        await asyncio.sleep(delay)
                    else:
                        raise
            raise Exception('Max retries exceeded getting blockhash')
        return self.blockhash


blockhash_cache = BlockhashCache(client)


async def create_wallet(count: int = 1) -> list[tuple[str, str]]:
    wallets = []
    for _ in range(count):
        keypair = Keypair()
        pubkey = keypair.pubkey()
        secretkey = bytes(keypair)
        wallets.append((str(pubkey), base58.b58encode(secretkey).decode()))
    return wallets


async def get_balance(wallet_private_key: str):
    private_key = base58.b58decode(wallet_private_key)
    keypair = Keypair.from_bytes(private_key)
    balance = await client.get_balance(keypair.pubkey())
    return balance.value


async def send_transfer(from_keypair: Keypair, to_pubkey_str: str, lamports: int):
    to_pubkey = Pubkey.from_string(to_pubkey_str)
    # Якщо to_pubkey_str — рядок публічного ключа, беремо як є, якщо приватний — декодуємо.

    transfer_instruction = transfer(
        TransferParams(
            from_pubkey=from_keypair.pubkey(),
            to_pubkey=to_pubkey,
            lamports=lamports,
        )
    )

    latest_blockhash = await blockhash_cache.get_blockhash()

    message = MessageV0.try_compile(
        payer=from_keypair.pubkey(),
        instructions=[transfer_instruction],
        address_lookup_table_accounts=[],
        recent_blockhash=latest_blockhash,
    )

    fee_response = await client.get_fee_for_message(message)
    transaction_fee = fee_response.value
    if transaction_fee is None:
        print('Не удалось получить комиссию!')
        return None

    amount_after_fee = lamports - transaction_fee
    if amount_after_fee <= 0:
        print('Недостаточно средств для отправки с учетом комиссии!')
        return None

    # Пересобираємо транзакцію з урахуванням комісії
    transfer_instruction = transfer(
        TransferParams(
            from_pubkey=from_keypair.pubkey(),
            to_pubkey=to_pubkey,
            lamports=amount_after_fee,
        )
    )
    message = MessageV0.try_compile(
        payer=from_keypair.pubkey(),
        instructions=[transfer_instruction],
        address_lookup_table_accounts=[],
        recent_blockhash=latest_blockhash,
    )
    transaction = VersionedTransaction(message, [from_keypair])

    # Відправка з повтором при 429
    for attempt in range(5):
        try:
            response = await client.send_transaction(transaction)
            console.print(
                f'[bold green]Транзакция отправлена Hash: {response.value}[/]'
            )
            return response.value
        except RPCException as e:
            if '429' in str(e) or 'Too Many Requests' in str(e):
                wait_sec = 3 * (attempt + 1)
                print(
                    f'Rate limited sending transaction, ждем {wait_sec} секунд... (попытка {attempt + 1})'
                )
                await asyncio.sleep(wait_sec)
            else:
                print('Ошибка при отправке транзакции:', e)
                return None
    print('Не удалось отправить транзакцию после нескольких попыток.')
    return None


async def money_distribution(amount: float):
    get_m_w = await get_main_wallet()
    main_wallet = Keypair.from_bytes(base58.b58decode(get_m_w.private_key))
    wallets = await get_wallets()
    money_on_one_wallet = amount / len(wallets)

    for wallet in wallets:
        await asyncio.sleep(0.5)
        wallet_keypair = Keypair.from_bytes(base58.b58decode(wallet.private_key))
        lamports = int(money_on_one_wallet * 1_000_000_000)
        await send_transfer(main_wallet, str(wallet_keypair.pubkey()), lamports)


async def money_withdrawal():
    get_m_w = await get_main_wallet()
    main_wallet = Keypair.from_bytes(base58.b58decode(get_m_w.private_key))
    wallets = await get_wallets()

    for wallet in wallets:
        wallet_keypair = Keypair.from_bytes(base58.b58decode(wallet.private_key))
        mint_balance = await get_token_balance(
            wallet_keypair.pubkey(), Pubkey.from_string(await get_token_address())
        )
        if mint_balance == 0:
            print(f'Кошелек {wallet_keypair.pubkey()} нету mint, пропускаем.')
            continue
        await asyncio.sleep(0.5)
        await sell_token(mint_balance, wallet.private_key)

    for wallet in wallets:
        wallet_keypair = Keypair.from_bytes(base58.b58decode(wallet.private_key))
        balance = await get_balance(wallet.private_key)
        mint_balance = await get_token_balance(
            wallet_keypair.pubkey(), Pubkey.from_string(await get_token_address())
        )
        if balance == 0 and mint_balance == 0:
            print(f'Кошелек {wallet_keypair.pubkey()} пустой, пропускаем.')
            continue
        await asyncio.sleep(0.5)
        await send_transfer(wallet_keypair, str(main_wallet.pubkey()), balance)


async def get_token_balance(wallet_pubkey: Pubkey, mint_pubkey: Pubkey):
    try:
        ata = get_associated_token_address(wallet_pubkey, mint_pubkey)

        resp = await client.get_token_account_balance(ata)

        if resp.value.ui_amount is None:
            return 0

        amount = resp.value.ui_amount
        return amount
    except Exception as e:
        return 0
