from brownie import network, config, accounts, MockV3Aggregator

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


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
