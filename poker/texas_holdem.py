import random
from functools import cmp_to_key
from poker.cards import StandardDeck
from poker.player import ManualPlayer, RandomPlayer

VALUES = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}

class TexasHoldem(object):
    def __init__(self, players):
        self.deck = StandardDeck()
        self.players = players
        self.pot = 0
        self.community = []
        self.dealer = random.choice(range(len(players)))

        self.small_blind_val = 5
        self.big_blind_val = 10

    def begin(self):
        self.deck.shuffle()
        for player in self.players:
            player.set_pocket([self.deck.deal(), self.deck.deal()])

    def get_winner(self, folded):
        players = []
        for i in range(len(self.players)):
            if i not in folded:
                players.append(self.players[i])

        player_hands = []
        for player in players:
            hands = power_sets(player.pocket + self.community)
            hands = [eval_hand(hand) for hand in hands]
            hands.sort(key=cmp_to_key(hand_cmp))

            player_hands.append((player, hands[-1]))

        player_hands.sort(key=cmp_to_key(lambda x, y: hand_cmp(x[1], y[1])))
        winning_hand = player_hands[-1][1]

        return list(map(lambda x: x[0], filter(lambda x: x[1] == winning_hand, player_hands)))

    def hand(self):
        # keep track of the current turn, folded players, and pot contributions
        turn = (self.dealer - 3) % len(self.players)
        contributions = {player: 0 for player in self.players}
        folded = set()

        # deal pocket cards
        self.begin()

        # take blinds
        small_blind = self.players[(self.dealer - 1) % len(self.players)]
        big_blind = self.players[(self.dealer - 2) % len(self.players)]

        small_blind_val = min(self.small_blind_val, small_blind.money)
        big_blind_val = min(self.big_blind_val, big_blind.money)

        small_blind.sub_money(small_blind_val)
        big_blind.sub_money(big_blind_val)
        self.pot += small_blind_val + big_blind_val
        contributions[small_blind] += small_blind_val
        contributions[big_blind] += big_blind_val

        # first betting round
        stake = max(small_blind_val, big_blind_val)
        last_raised = (self.dealer - 2) % len(self.players), stake
        big_turn = True
        all_in = False

        while turn != last_raised[0] or big_turn:
            if turn not in folded:
                player = self.players[turn]
                options = {'fold': (0, 0),
                           'call': (min(stake-contributions[player], player.money), min(stake-contributions[player], player.money))
                           }
                if not all_in and player.money >= stake-contributions[player]+max(1, last_raised[1]):
                    options['raise'] = (stake-contributions[player]+max(1, last_raised[1]), player.money)

                move = player.choose_move(options)

                if move[0] == 'fold':
                    folded.add(turn)
                elif move[0] == 'call' or move[0] == 'raise':
                    assert move[0] in options and options[move[0]][0] <= move[1] <= options[move[0]][1]
                    player.sub_money(move[1])
                    self.pot += move[1]
                    contributions[player] += move[1]

                    if move[0] == 'raise':
                        last_raised = turn, contributions[player] - stake
                        stake = contributions[player]

                        if move[1] == options[move[0]][1]:
                            all_in = True

                if self.players[turn] == big_blind and big_turn:
                    big_turn = False

                    if turn == last_raised and move[0] != 'raise':
                        break

            turn = (turn - 1) % len(self.players)

        # burn a card
        self.deck.deal()

        # deal 3 cards
        for _ in range(3):
            self.community.append(self.deck.deal())

        print(self.community)

        # second betting round
        def betting():
            contributions = {player: 0 for player in self.players}
            turn = (self.dealer - 1) % len(self.players)
            stake = 0
            last_raised = turn, 0
            first_turn = True
            all_in = False

            while turn != last_raised[0] or first_turn:
                if first_turn:
                    first_turn = False

                if turn not in folded:
                    player = self.players[turn]
                    if not stake:
                        options = {'check': (0, 0),
                                   'bet': (min(1, player.money), player.money)}
                    else:
                        options = {'fold': (0, 0),
                                   'call': (min(stake-contributions[player], player.money), min(stake-contributions[player], player.money))}
                        if not all_in and player.money >= stake - contributions[player] + max(1, last_raised[1]):
                            options['raise'] = (stake - contributions[player] + max(1, last_raised[1]), player.money)

                    move = player.choose_move(options)

                    if move[0] == 'fold':
                        folded.add(turn)
                    elif move[0] in ('call', 'raise', 'bet'):
                        assert move[0] in options and options[move[0]][0] <= move[1] <= options[move[0]][1]
                        player.sub_money(move[1])
                        self.pot += move[1]
                        contributions[player] += move[1]

                        if move[0] == 'raise' or move[0] == 'bet':
                            last_raised = turn, contributions[player] - stake
                            stake = contributions[player]

                            if move[1] == options[move[0]][1]:
                                all_in = True

                turn = (turn - 1) % len(self.players)

        betting()

        # burn a card
        self.deck.deal()

        # deal a card
        self.community.append(self.deck.deal())
        print(self.community)

        # third betting round
        betting()

        # burn a card
        self.deck.deal()

        # deal a card
        self.community.append(self.deck.deal())
        print(self.community)

        # final betting round
        betting()

        # give up the pot
        winners = self.get_winner(folded)
        prize = self.pot // len(winners)
        for player in winners:
            player.add_money(prize)
        self.pot = 0
        print('The winners are {} and they won {}'.format(winners, prize))

        self.deck.reset()

        self.dealer = (self.dealer - 1) % len(self.players)


def power_sets(cards):
    sets = []
    for i in range(len(cards)-1):
        for j in range(i+1, len(cards)):
            sets.append(cards[:i] + cards[i+1:j] + cards[j+1:])
    return sets


def eval_hand(cards):
    cards = [(VALUES[card[0]], card[1]) if isinstance(card[0], str) else card for card in cards]
    cards.sort(key=lambda x: x[0])
    values = [card[0] for card in cards]
    values.reverse()

    # check for a straight
    if cards[0][0] + 1 == cards[1][0] and cards[1][0] + 1 == cards[2][0] and cards[2][0] + 1 == cards[3][0] and cards[3][0] + 1 == cards[4][0]:
        if cards[0][1] == cards[1][1] == cards[2][1] == cards[3][1] == cards[4][1]:
            if cards[0][0] == 10:
                # royal flush
                return (10, *values)
            # straight flush
            return (9, *values)
        # straight
        return (5, *values)

    if cards[0][1] == cards[1][1] == cards[2][1] == cards[3][1] == cards[4][1]:
        # flush
        return (6, *values)

    counts = {}
    for card in cards:
        counts[card[0]] = counts.get(card[0], 0) + 1

    max_count = max(counts.values())
    if max_count == 4:
        # 4 of a kind
        return (8, *values)
    elif max_count == 3:
        if min(counts.values()) == 2:
            # full house
            return (7, *values)
        # three of a kind
        return (4, *values)
    elif max_count == 2:
        if list(counts.values()).count(2) == 2:
            # two pairs
            return (3, *values)
        # pair
        return (2, *values)
    else:
        # high card
        return (1, *values)


def hand_cmp(hand1, hand2):
    if hand1 == hand2:
        return 0

    for e1, e2 in zip(hand1, hand2):
        if e1 > e2:
            return 1
        elif e2 > e1:
            return -1


if __name__ == '__main__':
    players = [RandomPlayer('Player {}'.format(i), 100) for i in range(4)]
    players.append(ManualPlayer(name='Me', money=100))
    game = TexasHoldem(players)
    game.hand()
