from functools import cmp_to_key
import unittest

from poker.texas_holdem import TexasHoldem, power_sets, eval_hand, hand_cmp


class TestHandCmp(unittest.TestCase):
    def setUp(self):
        # self.game = TexasHoldem([])
        pass

    def select_hand(self, cards):
        hands = [eval_hand(hand) for hand in power_sets(cards)]
        hands.sort(key=cmp_to_key(lambda x, y: hand_cmp(x, y)))

        return hands[-1]

    def test_high_card(self):
        community = [(5, 'Diamonds'), (7, 'Diamonds'), (8, 'Hearts'), (10, 'Spades'), ('J', 'Clubs')]
        hand1 = [(2, 'Diamonds'), (4, 'Hearts')]
        hand2 = [(2, 'Diamonds'), ('K', 'Hearts')]

        best1 = self.select_hand(hand1 + community)
        best2 = self.select_hand(hand2 + community)

        best = sorted([best1, best2], key=cmp_to_key(hand_cmp))[-1]
        expected = (1, 13, 11, 10, 8, 7)

        self.assertEqual(best, expected)

    def test_high_card_tie1(self):
        community = [(5, 'Diamonds'), (7, 'Diamonds'), (8, 'Hearts'), (10, 'Spades'), ('J', 'Clubs')]
        hand1 = [(2, 'Diamonds'), (4, 'Hearts')]
        hand2 = [(2, 'Diamonds'), (3, 'Hearts')]

        best1 = self.select_hand(hand1 + community)
        best2 = self.select_hand(hand2 + community)

        expected = (1, 11, 10, 8, 7, 5)

        self.assertEqual(best1, expected)
        self.assertEqual(best2, expected)

    def test_high_card_tie2(self):
        community = [(5, 'Diamonds'), (7, 'Diamonds'), (8, 'Hearts'), (10, 'Spades'), ('J', 'Clubs')]
        hand1 = [(2, 'Diamonds'), ('K', 'Hearts')]
        hand2 = [(4, 'Diamonds'), ('K', 'Hearts')]

        best1 = self.select_hand(hand1 + community)
        best2 = self.select_hand(hand2 + community)

        expected = (1, 13, 11, 10, 8, 7)

        self.assertEqual(best1, expected)
        self.assertEqual(best2, expected)

    def test_low_pair(self):
        community = [(5, 'Diamonds'), (7, 'Diamonds'), (8, 'Hearts'), (10, 'Spades'), ('J', 'Clubs')]
        hand1 = [(2, 'Diamonds'), (2, 'Hearts')]
        hand2 = [('Q', 'Diamonds'), ('K', 'Hearts')]

        best1 = self.select_hand(hand1 + community)
        best2 = self.select_hand(hand2 + community)

        best = sorted([best1, best2], key=cmp_to_key(hand_cmp))[-1]
        expected = (2, 11, 10, 8, 2, 2)

        self.assertEqual(best, expected)

    def test_high_pair(self):
        community = [(5, 'Diamonds'), (7, 'Diamonds'), (8, 'Hearts'), (10, 'Spades'), ('J', 'Clubs')]
        hand1 = [(2, 'Diamonds'), (7, 'Hearts')]
        hand2 = [('J', 'Diamonds'), ('K', 'Hearts')]

        best1 = self.select_hand(hand1 + community)
        best2 = self.select_hand(hand2 + community)

        best = sorted([best1, best2], key=cmp_to_key(hand_cmp))[-1]
        expected = (2, 13, 11, 11, 10, 8)

        self.assertEqual(best, expected)

    def test_pair_kicker(self):
        community = [(5, 'Diamonds'), (7, 'Diamonds'), (8, 'Hearts'), (10, 'Spades'), ('J', 'Clubs')]
        hand1 = [(2, 'Diamonds'), ('J', 'Hearts')]
        hand2 = [('J', 'Diamonds'), ('K', 'Hearts')]

        best1 = self.select_hand(hand1 + community)
        best2 = self.select_hand(hand2 + community)

        best = sorted([best1, best2], key=cmp_to_key(hand_cmp))[-1]
        expected = (2, 13, 11, 11, 10, 8)

        self.assertEqual(best, expected)

    def test_pair_tie(self):
        community = [(5, 'Diamonds'), (7, 'Diamonds'), (8, 'Hearts'), (10, 'Spades'), ('J', 'Clubs')]
        hand1 = [(2, 'Diamonds'), ('J', 'Hearts')]
        hand2 = [('J', 'Diamonds'), (2, 'Hearts')]

        best1 = self.select_hand(hand1 + community)
        best2 = self.select_hand(hand2 + community)

        expected = (2, 11, 11, 10, 8, 7)

        self.assertEqual(best1, expected)
        self.assertEqual(best2, expected)


if __name__ == '__main__':
    unittest.main()
