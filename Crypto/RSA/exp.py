import pwn
import math
def getNEC(conn):
    message = conn.recvuntil('n = ', drop = True).strip()
    print message
    n = conn.recvuntil('e = ', drop = True).strip()
    print 'n = ', n
    e = conn.recvuntil('The Encypted secret:', drop=True).strip()
    print 'e = ', e
    conn.recvuntil('c = ')
    c = conn.recvuntil('Options:', drop = True).strip()
    print 'c = ', c
    message = conn.recvrepeat(3)
    print 'Options:\n' + message
    return int(n), int(e), int(c)

def getParity(conn, cc):
    conn.sendline('D')
    # print 'D'
    message = conn.recvuntil('message:')
    # print message
    conn.sendline(str(cc))
    # print cc
    message = conn.recvuntil('option:')
    # print message
    if 'odd' in message:
        return 1
    elif 'even' in message:
        return 0

def crack(conn):
    n, e, c = getNEC(conn)
    rounds = int(math.ceil(math.log(n, 2)))
    d = pow(2, e, n)
    cc = c
    eigenvalue = 0
    for i in range(rounds):
        if i % 256 == 0:
            print i
        cc = (cc * d) % n
        parity = getParity(conn, cc)
        eigenvalue = (eigenvalue << 1) + parity
    if eigenvalue == 0:
        return 0
    else:
        return n * eigenvalue / pow(2, rounds) + 1

def main():
    conn = pwn.remote('localhost', 12345)
    for i in range(10):
        mm = crack(conn)
        conn.sendline('G')
        message = conn.recvrepeat(1)
        print message
        conn.sendline(str(mm))
        print mm
        message = conn.recvuntil('Congratulations!')
        # message = conn.recvrepeat(3)
        print message
    message = conn.recvrepeat(2)
    print message

if __name__ == '__main__':
    main()
