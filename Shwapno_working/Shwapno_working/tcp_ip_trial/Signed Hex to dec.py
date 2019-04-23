beacon_data="0201060303AAFE1316AAFE21000A8F1B00000055CB0013FFF303F7"
hex_temp_data = beacon_data[42:46]
print("Value to be converted:", hex_temp_data)

import math

def hex_to_signed(source):
    """Convert a string hex value to a signed hexidecimal value.

    This assumes that source is the proper length, and the sign bit
    is the first bit in the first byte of the correct length.

    hex_to_signed("F") should return -1.
    hex_to_signed("0F") should return 15.
    """
    if not isinstance(source, str):
        raise ValueError("string type required")
    if 0 == len(source):
        raise ValueError("string is empty")
    sign_bit_mask = 1 << (len(source)*4-1)
    other_bits_mask = sign_bit_mask - 1
    value = int(source, 16)
    return -(value & sign_bit_mask) | (value & other_bits_mask)

output= hex_to_signed(hex_temp_data)
print(output)