from brownie import accounts, config, network, AntiMatterToken, MockV3Aggregator
from .utils import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS


class Contract:
    account = get_account()
    anti_matter = None
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
    def deploy_antimatter(cls, initial_supply: int = 100_000_000):
        print(cls.account)
        cls.anti_matter = AntiMatterToken.deploy(
            initial_supply,
            {"from": cls.account},
            publish_source=config["networks"][network.show_active()].get("verify"),
        )
        print(f"FundMe contract deployed to {cls.anti_matter.address}\n")
        print()


def main():
    Contract.deploy_antimatter(100_000_000)
