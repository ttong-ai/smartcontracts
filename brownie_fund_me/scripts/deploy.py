from brownie import accounts, config, network, FundMe, MockV3Aggregator
from .utils import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS


class Contract:
    account = get_account()
    fund_me = None
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_use_price_feed"
        ]
    else:
        print(f"Active network is {network.show_active()}")
        if len(MockV3Aggregator) == 0:
            mock = deploy_mocks(account)
            price_feed_address = mock.address
        else:
            print(f"Found previously deployed mock at {MockV3Aggregator[-1].address}")
            price_feed_address = MockV3Aggregator[-1].address

    @classmethod
    def deploy_fund_me_contract(cls):
        print(cls.account)
        cls.fund_me = FundMe.deploy(
            cls.price_feed_address,
            {"from": cls.account},
            publish_source=config["networks"][network.show_active()].get("verify"),
        )
        print(f"FundMe contract deployed to {cls.fund_me.address}\n")
        eth_price = cls.fund_me.getETHPrice()
        print(f"Current ETH price in USD: {eth_price/1e8:.2f}\n")
        current_usd_balance = cls.fund_me.getUSDValue()
        print(f"Current USD balance: {current_usd_balance:.2f}\n")
        print()

    @classmethod
    def store_simple_storage(cls, value: int = 100):
        transaction = cls.simple_storage.store(value, {"from": cls.account})
        transaction.wait(1)
        stored_value = cls.simple_storage.retrieve_view()
        print(stored_value)
        print()


def main():
    Contract.deploy_fund_me_contract()
