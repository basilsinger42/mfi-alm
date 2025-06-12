from mfi_alm.assets.asset import Asset

def test_asset() -> None:
    asset = Asset(market_price=100.0, growth_rate=0.05)
    assert True