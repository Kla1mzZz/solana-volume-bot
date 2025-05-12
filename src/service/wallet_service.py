from solders.message import Message
from solders.keypair import Keypair
from solders.hash import Hash
from solders.transaction import Transaction
from solders.pubkey import Pubkey
from solders.system_program import transfer, TransferParams

import json

def create_wallet():
    keypair = Keypair()
    pubkey = keypair.pubkey()
    secret = keypair.to_bytes()  # 64-byte seed
    return keypair, pubkey, secret

def save_wallet_to_file(keypair: Keypair, filename="wallet.json"):
    secret = list(keypair.to_bytes())  # Convert bytes to list of ints
    with open(filename, "w") as f:
        json.dump(secret, f)
        
def load_wallet_from_file(filename="wallet.json") -> Keypair:
    with open(filename, "r") as f:
        secret = json.load(f)
    return Keypair.from_bytes(bytes(secret))

# Create and save a wallet
kp, pubkey, secret = create_wallet()
print("Public Key:", pubkey)
save_wallet_to_file(kp)

# Load the wallet again
loaded_kp = load_wallet_from_file()
print("Loaded Public Key:", loaded_kp.pubkey())



# def create_transfer_transaction(from_kp: Keypair, to_pubkey: Pubkey, lamports: int) -> Transaction:
#     ix = transfer(TransferParams(
#         from_pubkey=from_kp.pubkey(),
#         to_pubkey=to_pubkey,
#         lamports=lamports
#     ))
#     msg = Message([ix], from_kp.pubkey())
#     blockhash = Hash.default()
#     tx = Transaction([from_kp], msg, blockhash)
#     return tx

# Приклад
# receiver = Pubkey.from_string("11111111111111111111111111111111")
# tx = create_transfer_transaction(keypair, receiver, 1000000)
# print("Transaction created:", tx)

