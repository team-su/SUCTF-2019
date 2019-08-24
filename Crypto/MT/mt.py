from Crypto.Random import random
from Crypto.Util import number
from flag import flag

def convert(m):
    m = m ^ m >> 13
    m = m ^ m << 9 & 2029229568
    m = m ^ m << 17 & 2245263360
    m = m ^ m >> 19
    return m

def transform(message):
    assert len(message) % 4 == 0
    new_message = ''
    for i in range(len(message) / 4):
        block = message[i * 4 : i * 4 +4]
        block = number.bytes_to_long(block)
        block = convert(block)
        block = number.long_to_bytes(block, 4)
        new_message += block
    return new_message

transformed_flag = transform(flag[5:-1].decode('hex')).encode('hex')
print 'transformed_flag:', transformed_flag
# transformed_flag: 641460a9e3953b1aaa21f3a2


