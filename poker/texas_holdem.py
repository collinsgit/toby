from poker.cards import StandardDeck


class TexasHoldem(object):
    def __init__(self, players):
        self.deck = StandardDeck()
        self.players = players
        self.pot = 0
        self.community = []

    def begin(self):
        self.deck.shuffle()
        for player in self.players:
            player.set_hand([self.deck.deal(), self.deck.deal()])



