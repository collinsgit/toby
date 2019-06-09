import random


class Player(object):
    def __init__(self, name='Player', money=0):
        self.name = name
        self.pocket = []
        self.money = money

    def add_money(self, money):
        assert money >= 0
        self.money += money

    def sub_money(self, money):
        assert 0 <= money <= self.money
        self.money -= money

    def choose_move(self, moves):
        move = random.choice(moves.keys())
        return move, moves[move][0]

    def set_pocket(self, pocket):
        self.pocket = pocket


class ManualPlayer(Player):
    def choose_move(self, moves):
        print(self.pocket)
        for move in moves:
            print('{}: {}'.format(move, moves[move]))

        response = input('Select a move: ').split()
        response = (response, 0) if len(response) == 1 else response

        return response[0], int(response[1])


class RandomPlayer(Player):
    def choose_move(self, moves):
        move = random.choice(list(moves.keys()))
        value = random.randint(*moves[move])

        print('{}: {} {}'.format(self.name, move, value))
        return move, value
