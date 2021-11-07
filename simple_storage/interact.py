from dotenv import load_dotenv
import json
import os
from time import sleep
from web3 import Web3

load_dotenv()

CWD = os.path.dirname(__file__)


with open(os.path.join(CWD, "compiled_code.json"), "r") as file:
    compiled_sol = json.load(file)

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
# chain_id = 1337
# my_address = "0x669135d482892ef79b4DA5c49A37d12458697Cea"
# private_key = os.getenv("PRIVATE_KEY")

w3 = Web3(Web3.HTTPProvider("https://kovan.infura.io/v3/89a1e45a907f42258e827eaffb89b640"))
chain_id = 42
my_address = "0xb42fc2eb1c141546a87C55D7ACe661F234FFf607"
private_key = os.getenv("PRIVATE_KEY")

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(f"{nonce = }\n")

# Here is the deployed contract address on the blockchain
contract_address = "0xa30A1161b46ED8FA4C28DF069367e13D0f8B959a"

simple_storage = w3.eth.contract(address=contract_address, abi=abi)
print("Current value in storage: ", simple_storage.functions.retrieve_view().call())

# this wouldn't work
# print(simple_storage.functions.store(100).call())

# Need to build another transaction with the contract
print("Updating contract...")
try:
    store_transaction = simple_storage.functions.store(209).buildTransaction(
        {"chainId": chain_id, "from": my_address, "nonce": nonce}
    )
    signed_store_txn = w3.eth.account.sign_transaction(
        store_transaction, private_key=private_key
    )
    tx_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # print(tx_receipt)
except Exception as e:
    print("ERROR:", e)
print("Contract updated")

# Check the stored value again
print("Updated value in storage", simple_storage.functions.retrieve_view().call())
