from guess_game import max_round


class Ticket:
    def __init__(self, number):
        self.number = number

    def __eq__(self, other):
        if type(self) == type(other) and self.number == other.number:
            return True
        else:
            return False

    def is_valid(self):
        assert type(self.number) == int

        if max_round >= self.number >= 0:
            return True
        else:
            return False
