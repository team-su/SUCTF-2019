from Crypto.Hash import MD5
from Crypto.PublicKey import DSA
from Crypto.Util import number
from Crypto.Random import random
import gmpy2 as gm

key = DSA.generate(1024)

m1 = 'hello'
m2 = 'world'

h1 = number.bytes_to_long(MD5.new(m1).digest())
h2 = number.bytes_to_long(MD5.new(m2).digest())

k = random.getrandbits(50)

(r1, s1) = key.sign(h1, k)
(r2, s2) = key.sign(h2, k)

print (r1, s1)
print (r2, s2)

print 'begin to crack...'
p = key.p
q = key.q
g = key.g

x = (s2 * h1 - s1 * h2) * gm.invert(s1 * r1 - s2 * r1, q) % q
assert x == key.x
print 'ok'
