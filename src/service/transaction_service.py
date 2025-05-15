from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID

import base58

solana_client = Client("https://api.mainnet-beta.solana.com")


async def buy_token(mint_address, amount, buyer_wallet, private_key) -> None:
    wallet = Keypair.from_bytes(base58.b58decode(private_key))
    mint_pubkey = Pubkey(mint_address)
    token = Token(
        conn=solana_client,
        pubkey=mint_pubkey,
        program_id=TOKEN_PROGRAM_ID,
        payer=buyer_wallet
    )

    buyer_token_account = token.create_associated_token_account(buyer_wallet.public_key)

    print(f"Куплено {amount} токенов {mint_address}")

async def sell_token(mint_address, amount, seller_wallet) -> None:
    mint_pubkey = Pubkey(mint_address)
    token = Token(
        conn=solana_client,
        pubkey=mint_pubkey,
        program_id=TOKEN_PROGRAM_ID,
        payer=seller_wallet
    )

    seller_token_account = token.get_accounts_by_owner(seller_wallet.public_key).value[0].pubkey


    print(f"Продано {amount} токенов {mint_address}")
