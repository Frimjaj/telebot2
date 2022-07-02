from random import shuffle


class Card:
    """
    Класс игральной карты.
    """

    card_values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    card_suits = ["♥", "♦", "♣", "♠"]

    def __init__(self, value, suit):
        self.__value = value
        self.__suit = suit

    @property
    def value(self):
        return self.__value

    @property
    def suit(self):
        return self.__suit

    def display_card_info(self):
        return f"{self.suit}{self.value}"

    def __str__(self):
        return f"{self.suit}{self.value}"


class Deck:
    """
    Класс колоды карт.
    """

    @staticmethod
    def create_deck():

        deck = [Card(value, suit) for value in Card.card_values for suit in Card.card_suits]
        return deck

    def __init__(self):
        self.__deck = self.create_deck()

    @property
    def deck(self):
        return self.__deck

    def shuffle_deck(self):
        shuffle(self.deck)

    def pop_card_from_deck(self):
        return self.deck.pop(0)

    def double_deck(self):
        self.__deck = [Card(value, suit) for value in Card.card_values for suit in Card.card_suits] * 2
