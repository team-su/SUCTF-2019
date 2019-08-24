from guess_game.Ticket import Ticket
from guess_game.RestrictedUnpickler import restricted_loads
from struct import unpack
from guess_game import game
import sys

with open('/flag', 'r') as f:
    flag = f.read().strip()


def read_length(obj):
    return unpack('>I', obj)


def stdin_read(length):
    return sys.stdin.buffer.read(length)


try:
    while not game.finished():
        length = stdin_read(4)
        length, = read_length(length)

        ticket = stdin_read(length)
        ticket = restricted_loads(ticket)

        assert type(ticket) == Ticket

        if not ticket.is_valid():
            print('The number is invalid.')
            game.next_game(Ticket(-1))
            continue

        win = game.next_game(ticket)
        if win:
            text = "Congratulations, you get the right number!"
        else:
            text = "Wrong number, better luck next time."
        print(text)

    if game.is_win():
        text = "Game over! You win all the rounds, here is your flag %s" % flag
    else:
        text = "Game over! You got %d/%d." % (game.win_count, game.round_count)
    print(text)

except Exception:
    print('Houston, we got a problem.')
