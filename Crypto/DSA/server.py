#_*_coding:utf-8_*_
#@Time:     2019/3/31 10:10
#@Author:   xwg
#@FileName: xx11.py

import os
import socket
import threading
import time
import SocketServer
from Crypto.PublicKey import DSA
from Crypto.Random import random
from Crypto.Hash import MD5
from Crypto.Util import number
from flag import flag


host, port = 'localhost', 10011
BUFF_SIZE = 1024

BLOCK_SIZE = 16

class MySockServer(SocketServer.BaseRequestHandler):
    def handle(self):
        key = DSA.generate(1024)
        poem = ['When I do count the clock that tells the time', 'And see the brave day sunk in hideous night',
                'When I behold the violet past prime', "And sable curls all silver'd o'er with white",
                'When lofty trees I see barren of leaves', 'Which erst from heat did canopy the herd',
                "And summer's green, all girded up in sheaves", 'Born on the bier with white and bristly beard',
                'Then of thy beauty do I question make', 'That thou among the wastes of time must go',
                'Since sweets and beauties do themselves forsake', 'And die as fast as they see others grow'
                ]

        self.request.send('\n')
        self.request.send('\n')
        self.request.send('\n')
        self.request.send("******************************************************************\n")
        self.request.send("* Challenge created by xwg                                       *\n")
        self.request.send("******************************************************************\n")
        self.request.send('\n')
        self.request.send('\n')
        self.request.send('\n')

        self.request.send("I love to collect signature, can you sign something for me?")
        self.request.recv(4)
        self.request.send('\n')
        self.request.send("p:"+str(key.p))
        self.request.send('\n')
        self.request.send('\n')
        self.request.send("q:" + str(key.q))
        self.request.send('\n')
        self.request.send('\n')
        self.request.send("g:" + str(key.g))
        self.request.send('\n')
        self.request.send('\n')
        # self.request.send("x:" + str(key.x))
        # self.request.send('\n')
        # self.request.send('\n')
        self.request.send("y:" + str(key.y))
        self.request.send('\n')
        self.request.send('\n')

        self.request.send("let me show you some before:")
        self.request.recv(4)
        ks = [0] * (len(poem))
        for i in range(len(ks)):
            ks[i] = random.randint(1, key.q - 1)
        for i in poem:
            k = ks[random.randint(1, len(poem) - 1)]
            print k
            j = number.bytes_to_long(MD5.new(i).digest())
            msg = key.sign(j, k)
            self.request.send(i)
            self.request.send('\nIts MD5 digest: ' + str(j))
            self.request.send('\n')
            self.request.send(str(msg))
            self.request.send('\n')
            self.request.send('\n')
            self.request.send("------------------------------------------------------------------------")
            self.request.send('\n')
            self.request.send('\n')



        self.request.send("please sign [And nothing 'gainst Time's scythe can make defence] for me:")
        self.request.send("\nIts MD5 digest is:")
        self.request.send(str(number.bytes_to_long(MD5.new("And nothing 'gainst Time's scythe can make defence").digest())))
        rs = self.request.recv(BUFF_SIZE).strip()

        try:
            sign = list(rs.replace("(", "").replace(")", "").replace("L", "").replace(",", '').split())
            for i in range(len(sign)):
                sign[i] = int(sign[i])
            sign = tuple(sign)

            if key.verify(MD5.new("And nothing 'gainst Time's scythe can make defence").digest(), sign):
                self.request.send("Congratulations!")
                self.request.send("\n")

                self.request.send(flag)
            else:
                self.request.send("Your signature is invalid.")
        except ValueError:
            self.request.send('wrong format')


def main():
    s = SocketServer.ThreadingTCPServer((host, port), MySockServer)
    s.serve_forever()

if __name__ == '__main__':
    main()