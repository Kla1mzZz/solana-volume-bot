import base58
from pumpswap_sdk import PumpSwapSDK
from solders.pubkey import Pubkey
from solders.keypair import Keypair

# from database import get_wallets

import asyncio


sdk = PumpSwapSDK()

mint = "7Tx8qTXSakpfaSFjdztPGQ9n2uyT1eUkYz7gYxxopump"
user_private_key = "4sBPJAhFVG67HDZo2Eju3KrciiK9c3GrLC2393bjHeBX29qAf7M18FqpARdd95DrB2rUCYn4nBzpnLNSVd17APQp"


async def get_token_price():
    token_price = await sdk.get_token_price(mint)
    print(f"Token Price: {token_price}")    

# async def buy_tokens():
#     wallets = await get_wallets()
#     for wallet in wallets:
#         private_key = Keypair().from_bytes(base58.b58decode(wallet.private_key))
#         user_private_key = str(private_key)
#         print(user_private_key)
#         sol_amount = 0.0001  # Amount of SOL to spend
#         result = await sdk.buy(mint, sol_amount, user_private_key)
#         print(result)


# async def sell_token():
#     wallets = await get_wallets()
#     for wallet in wallets:
#         private_key = Keypair().from_bytes(base58.b58decode(wallet.private_key))
#         user_private_key = str(private_key)
#         print(user_private_key) 
#         token_amount = 10.0  # Amount of tokens to sell
#         result = await sdk.sell(mint, token_amount, user_private_key)
#         print(result)

# # asyncio.run(buy_tokens())
asyncio.run(get_token_price())


