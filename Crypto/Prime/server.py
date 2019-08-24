from Crypto.Random import random
import util
import flag

from random import choice
from string import hexdigits
from hashlib import md5

def proof_of_work():
    part_hash = "".join([choice(hexdigits) for _ in range(5)]).lower()
    salt = "".join([choice(hexdigits) for _ in range(4)]).lower()
    print '[*] Please find a string that md5(str + ' + salt + ')[0:5] == ' + part_hash
    string = raw_input('> ')
    if (md5(string + salt).hexdigest()[:5] != part_hash):
        print('[-] Wrong hash, exit...')
        exit(0)

def main():
    N = 4
    scale = 2048
    ns = util.generateNs(N, scale)
    ms = [0] * N
    for i in range(len(ms)):
        ms[i] = random.randint(0, ns[i] - 1)
    cs = [0] * N
    for i in range(N):
        cs[i] = pow(ms[i], ns[i], ns[i])
        print 'cs[%d] = %s'%(i, hex(cs[i]))
        print 'ns[%d] = %s'%(i, hex(ns[i]))

    for i in range(N):
        x = raw_input('ms[%d] = '%i).strip()
        assert int(x, 16) == ms[i]

    print flag.flag

if __name__ == '__main__':
    proof_of_work()
    try:
        main()
    except:
        print 'Error!'
