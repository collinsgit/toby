import random


class Deck(object):
    ranks = []
    suits = []

    def __init__(self):
        self.deck = []
        self.reset()

    def reset(self):
        self.deck = [(rank, suit) for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        if self.deck:
            return self.deck.pop()
        else:
            raise StopIteration


class StandardDeck(Deck):
    ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
