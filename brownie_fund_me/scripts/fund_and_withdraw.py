from brownie import network, config, FundMe
from .utils import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from time import sleep


class Agent:
    def __init__(self, num: int = 1, contract: int = -1):
        self.account = get_account(num)
        print(f"Agent address: {self.account}")
        self.fund_me = FundMe[contract]
        print(f"Found deployed smart contract: {self.fund_me}")

    def get_balance(self):
        current_usd_balance = self.fund_me.getUSDValue()
        print(f"Current contract balance in USD: {current_usd_balance}")

    def fund(self, amount=50):
        print("Before funding transaction ...")
        self.get_balance()
        eth_price = self.fund_me.getETHPrice() / 1e8
        wei = int(amount / eth_price * 1e18)
        tx = self.fund_me.fund({"from": self.account, "value": wei})
        tx.wait(1)
        sleep(5)
        print(f"{self.account} funded USD {amount}")
        self.get_balance()

    def withdraw(self):
        print("Before withdrawing...")
        self.get_balance()
        tx = self.fund_me.withdraw({"from": self.account})
        tx.wait(1)
        sleep(5)
        print("After withdrawing...")
        self.get_balance()


def main():
    import random

    random.seed(42)

    agents = []
    for i in range(10):
        agents.append(Agent(i))

    for i in range(0, 10)[::-1]:
        if i > 0:
            agents[i].fund(amount=random.random() * 80 + 20)
        else:
            agents[0].withdraw()
            agents[0].get_balance()
