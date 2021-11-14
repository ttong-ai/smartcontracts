from brownie import network, config, accounts, MockV3Aggregator
from copy import copy
from cryptography.fernet import Fernet
import random


LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

def check_hashseed() -> bool:
    if hash("GOD") == -3890164749404887474:
        print("Hash seed confirmed.")
        return True
    else:
        print("Hash seed incorrect.")
        return False

def permutate(input: str, key: str = "test"):
    """Input should be a space delimited word string"""
    if not check_hashseed():
        print("Cannot continue with permutation")
        return
    words = [w.strip() for w in input.split()]
    wc = len(words)
    seq_orig = list(range(wc))
    seq = copy(seq_orig)
    random.seed(hash(key))
    random.shuffle(seq)
    return " ".join([words[i] for i in seq])

def reverse_permutate(input: str, key: str = "test"):
    """Input should be a space delimited word string"""
    if not check_hashseed():
        print("Cannot continue with permutation")
        return
    words = [w.strip() for w in input.split()]
    wc = len(words)
    seq_orig = list(range(wc))
    seq = copy(seq_orig)
    random.seed(hash(key))
    random.shuffle(seq)
    tp = list(zip(seq_orig, seq))
    tp.sort(key=lambda x: x[1])
    seq_rev = [t[0] for t in tp]
    return " ".join([words[i] for i in seq_rev])


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)



def get_account(num: int = 0):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[num]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks(account):
    print(f"Deploying Mocks...")
    mock = MockV3Aggregator.deploy(12, 456789000000, {"from": account})
    print(f"Mock price feed deployed at: {mock.address}")
    return mock
