from brownie import accounts, SimpleStorage


def test_updating_storage():
    # Deploy
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # Act
    expected = 15
    simple_storage.store(expected, {"from": account})
    # Assert
    assert simple_storage.retrieve_view() == expected
