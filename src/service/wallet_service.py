import base58
import asyncio

from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solders.transaction import VersionedTransaction
from solders.system_program import TransferParams, transfer
from solders.message import MessageV0
from solana.rpc.core import RPCException
from spl.token.async_client import AsyncToken
from spl.token.constants import TOKEN_PROGRAM_ID

from database import get_wallets, get_main_wallet
from utils.styles import console


client = AsyncClient('https://api.devnet.solana.com')


async def create_wallet(count: int = 1) -> list[tuple[str, str]]:
    wallets = []
    for i in range(count):
        keypair = Keypair()
        pubkey = keypair.pubkey()
        secretkey = keypair.to_bytes()
        wallet = (str(pubkey), base58.b58encode(secretkey).decode())
        wallets.append(wallet)

    return wallets


async def get_balance(wallet_private_key: str):
    private_key = base58.b58decode(wallet_private_key)

    keypair = Keypair.from_bytes(private_key)

    balance = await client.get_balance(keypair.pubkey())

    return balance.value


async def money_distibution(amount: float):
    get_m_w = await get_main_wallet()
    main_wallet = Keypair.from_bytes(base58.b58decode(get_m_w.private_key))
    wallets = await get_wallets()
    money_on_one_wallet = amount / len(wallets)

    for wallet in wallets:
        wallet = Keypair().from_bytes(base58.b58decode(wallet.private_key))
        transfer_instruction = transfer(
            TransferParams(
                from_pubkey=main_wallet.pubkey(),
                to_pubkey=wallet.pubkey(),
                lamports=int(money_on_one_wallet * 1_000_000_000),
            )
        )

        latest_blockhash = (await client.get_latest_blockhash()).value.blockhash

        message = MessageV0.try_compile(
            payer=main_wallet.pubkey(),
            instructions=[transfer_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=latest_blockhash,
        )

        fee_response = await client.get_fee_for_message(message)
        transaction_fee = fee_response.value

        if transaction_fee is None:
            print('Не удалось получить комиссию!')
            return None

        amount_in_lamports = int(money_on_one_wallet * 1_000_000_000) - transaction_fee
        if amount_in_lamports <= 0:
            print('Недостаточно средств для отправки с учетом комиссии!')
            return None

        transfer_instruction = transfer(
            TransferParams(
                from_pubkey=main_wallet.pubkey(),
                to_pubkey=wallet.pubkey(),
                lamports=amount_in_lamports,
            )
        )

        message = MessageV0.try_compile(
            payer=main_wallet.pubkey(),
            instructions=[transfer_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=latest_blockhash,
        )

        transaction = VersionedTransaction(message, [main_wallet])

        try:
            response = await client.send_transaction(transaction)
            console.print(
                f'[bold green]Транзакция отправлена Hash: {response.value}[/]'
            )

        except RPCException as e:
            print('Ошибка при отправке транзакции:', e)
            return None

async def money_withdrawal():
    get_m_w = await get_main_wallet()
    main_wallet = Keypair.from_bytes(base58.b58decode(get_m_w.private_key))
    wallets = await get_wallets()
    

    for wallet in wallets:
        money_on_one_wallet = await get_balance(wallet.private_key)
        wallet = Keypair().from_bytes(base58.b58decode(wallet.private_key))
        
        transfer_instruction = transfer(
            TransferParams(
                from_pubkey=wallet.pubkey(),
                to_pubkey=main_wallet.pubkey(),
                lamports=money_on_one_wallet,
            )
        )

        latest_blockhash = (await client.get_latest_blockhash()).value.blockhash

        message = MessageV0.try_compile(
            payer=wallet.pubkey(),
            instructions=[transfer_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=latest_blockhash,
        )

        fee_response = await client.get_fee_for_message(message)
        transaction_fee = fee_response.value

        if transaction_fee is None:
            print('Не удалось получить комиссию!')
            return None

        amount_in_lamports = money_on_one_wallet - transaction_fee
        if amount_in_lamports <= 0:
            print('Недостаточно средств для отправки с учетом комиссии!')
            return None

        transfer_instruction = transfer(
            TransferParams(
                from_pubkey=wallet.pubkey(),
                to_pubkey=main_wallet.pubkey(),
                lamports=amount_in_lamports,
            )
        )

        message = MessageV0.try_compile(
            payer=wallet.pubkey(),
            instructions=[transfer_instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=latest_blockhash,
        )

        transaction = VersionedTransaction(message, [wallet])

        try:
            response = await client.send_transaction(transaction)
            console.print(
                f'[bold green]Деньги получены Hash: {response.value}[/]'
            )

        except RPCException as e:
            print('Ошибка при отправке транзакции:', e)
            return None
