# Evmos wallet

Evmos wallet utils for python3.

## Installation

```sh
pip install evmoswallet
```

## Usage

```python
from evmoswallet import Wallet

wallet = Wallet(seed)
seed = 'report spend crisp crisp world shock morning hour spoon problem one hole program piano donkey width today view canoe clap brick bundle rose book'

print(wallet.eth_address) # "0xe7e3654bc1ea915e7216d8193ef8dd7d5dae987f"
print(wallet.evmos_address) # "evmos1ul3k2j7pa2g4uuskmqvna7xa04w6axrl85alz5"
print(wallet.private_key) # bytes.fromhex("8721109b7244925c0480f4172546b8b53dfe87845274070fbe8e6da739d1b813")

msg = bytes(...) # protobuf message
signed = wallet.sign(msg)
```

## References

[pywallet](https://github.com/ranaroussi/pywallet/)
[tow1](https://pypi.org/project/two1/)
