# Welcome to crypto-stocks

Here are some instructions how to use this libraly

#### How to import library

```python
import crypto-stocks
```

#### How to get price for crypto currency from Binance

```python
price_binance = Binance('crypto_name', 'fiat_currency')
#example:
price_binance = Binance('btc', 'usd')
```

#### How to get price for crypto currency from Coinbase

```python
price_coinbase = Coinbase('crypto_name', 'fiat_currency')
#example:
price_coinbase = Coinbase('btc', 'usd')
```

#### How to get price for crypto currency from FTX

```python
price_ftx = FTX('crypto_name', 'fiat_currency')
#example:
price_ftx = FTX('btc', 'usd')
```

#### How to get price for crypto currency from Kraken

```python
price_kraken = Kraken('crypto_name', 'fiat_currency')
#example:
price_kraken = Kraken('btc', 'usd')
```

#### How to get price for crypto currency from BitStamp

```python
price_bitstamp = BitStamp('crypto_name', 'fiat_currency')
#example:
price_bitstamp = BitStamp('btc', 'usd')
```
