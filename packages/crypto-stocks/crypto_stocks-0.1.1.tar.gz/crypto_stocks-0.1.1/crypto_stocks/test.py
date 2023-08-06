from .get_price import Binance, Coinbase, FTX, Kraken, BitStamp

for i in range(100):
    print(Binance('btc', 'usd'))

    print(Coinbase('btc', 'usd'))

    print(FTX('btc', 'usd'))

    print(Kraken('btc', 'usd'))

    print(BitStamp('btc', 'usd'))