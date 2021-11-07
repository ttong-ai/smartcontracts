from brownie import SimpleStorage, accounts, config


def read_contract():
    # Obtain the latest deployed contract
    simple_storage = SimpleStorage[-1]
    print(simple_storage.retrieve_view())


def main():
    read_contract()
