from brownie import accounts, config, SimpleStorage


class Contract:

    # account = accounts[0]
    # account = accounts.load("mm2-account")
    account = accounts.add(config["wallets"]["from_key"])
    simple_storage = None

    @classmethod
    def deploy_simple_storage(cls):
        print(cls.account)
        cls.simple_storage = SimpleStorage.deploy({"from": cls.account})
        stored_value = cls.simple_storage.retrieve_view()
        print(stored_value)
        print()

    @classmethod
    def store_simple_storage(cls, value: int = 100):
        transaction = cls.simple_storage.store(value, {"from": cls.account})
        transaction.wait(1)
        stored_value = cls.simple_storage.retrieve_view()
        print(stored_value)
        print()


def main():
    Contract.deploy_simple_storage()
    Contract.store_simple_storage(444)
    Contract.store_simple_storage(777)
