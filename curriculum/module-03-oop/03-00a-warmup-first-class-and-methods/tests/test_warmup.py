from warmup import SimpleWallet


def test_deposit_and_withdraw_success() -> None:
    wallet = SimpleWallet(100)
    wallet.deposit(50)
    assert wallet.withdraw(40) is True
    assert wallet.balance == 110


def test_withdraw_insufficient_funds() -> None:
    wallet = SimpleWallet(20)
    assert wallet.withdraw(50) is False
    assert wallet.balance == 20
