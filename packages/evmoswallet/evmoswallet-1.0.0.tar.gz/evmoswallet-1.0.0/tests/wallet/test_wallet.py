from evmoswallet import Wallet


def test_wallet():
    seed = (
        'report spend crisp crisp world shock morning hour spoon problem one hole program piano donkey width today view canoe clap brick bundle rose book'  # NOQA: E501
    )
    wallet = Wallet(seed)

    assert wallet.eth_address == '0xe7e3654bc1ea915e7216d8193ef8dd7d5dae987f'
    assert wallet.evmos_address == 'evmos1ul3k2j7pa2g4uuskmqvna7xa04w6axrl85alz5'
    assert wallet.private_key == bytes.fromhex('8721109b7244925c0480f4172546b8b53dfe87845274070fbe8e6da739d1b813')


def test_sign():
    seed = (
        'garment seat help gallery ride divide truth smooth end chunk ten cross badge want vehicle mirror dismiss remind crouch base crouch palm leader dinner'  # NOQA: E501
    )

    wallet = Wallet(seed)
    input = bytes([
        177, 240, 144, 132, 71, 52, 192, 86, 100, 12, 4, 148, 127, 217, 62, 166, 254, 121, 39, 134, 16, 193, 151, 209,
        7, 181, 85, 226, 30, 52, 62, 7
    ])
    output = bytes([
        245, 167, 163, 221, 231, 60, 6, 188, 101, 237, 235, 104, 205, 107, 214, 180, 27, 213, 16, 161, 154, 8, 180, 244,
        1, 136, 124, 205, 163, 59, 93, 3, 35, 24, 142, 200, 223, 233, 21, 51, 199, 110, 174, 174, 237, 115, 2, 104, 131,
        241, 235, 156, 137, 31, 182, 244, 214, 186, 161, 183, 140, 131, 141, 233, 0
    ])

    assert wallet.sign(input) == output
