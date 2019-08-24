from random import randint
from guess_game.Ticket import Ticket
from guess_game import max_round, number_range


class Game:
    def __init__(self):
        number = randint(0, number_range)
        self.curr_ticket = Ticket(number)
        self.round_count = 0
        self.win_count = 0

    def next_game(self, ticket):
        win = False
        if self.curr_ticket == ticket:
            self.win_count += 1
            win = True

        number = randint(0, number_range)
        self.curr_ticket = Ticket(number)
        self.round_count += 1

        return win

    def finished(self):
        return self.round_count >= max_round

    def is_win(self):
        return self.win_count == max_round
