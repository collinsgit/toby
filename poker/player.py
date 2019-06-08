import random


class Player(object):
    def __init__(self, money=0):
        self.hand = []
        self.money = money

    def add_money(self, money):
        assert money >= 0
        self.money += money

    def sub_money(self, money):
        assert 0 <= money <= self.money
        self.money -= money

    def choose_move(self, moves):
        return random.choice(moves)

    def set_hand(self, hand):
        self.hand = hand


class ManualPlayer(Player):
    def choose_move(self, moves):
        for i, move in enumerate(moves):
            print('{}: {}'.format(i, move))
        return moves[int(input('Select a move:'))]
