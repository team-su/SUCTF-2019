from Crypto.PublicKey import RSA
from Crypto.Random import random
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

options = 'Options:\n\
    [D] Decrypt a message.\n\
    [G] Guess the secret.\n\
    [Q] Quit.'
def challenge():
    k = RSA.generate(2048)
    m = random.randint(0, k.n-1)
    print 'n = %d' % k.n
    print 'e = %d' % k.e
    c = k.encrypt(m, 0)
    print 'The Encypted secret:'
    print 'c = %d' % c[0]
    while True:
        print options
        option = raw_input('Please input your option:').strip().upper()
        if option == 'D':
            cc = int(raw_input('Your encrypted message:').strip())
            mm = k.decrypt(cc)
            if mm & 1 == 1:
                print 'The plain of your decrypted message is odd!'
            else:
                print 'The plain of your decrypted message is even!'
        elif option == 'G':
            mm = int(raw_input('The secret:').strip())
            if mm == m:
                print 'Congratulations!'
                return True
            else:
                print 'Wrong! Bye~'
                return False
        else:
            print 'GoodBye~'
            return False

if __name__ == '__main__':
    proof_of_work()
    rounds = 10
    print 'Guess the Secrets %d times, Then you will get the flag!' % rounds
    good = 0
    try:
        for i in range(rounds):
            print 'Round %d' % (i + 1)
            if challenge():
                good += 1
            else:
                break
    except Exception:
        print 'Error! Bye~'

    if good == rounds:
        print flag.flag
