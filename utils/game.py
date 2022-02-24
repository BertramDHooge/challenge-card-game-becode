from utils.player import Player
from typing import List
from utils.card import Deck, Card, UnoCard
from random import shuffle, choice
from time import sleep


class Board:
    """
    Class that describes a (game)board upon which a game can be played.
    """

    def __init__(self, players: List[Player], deck: Deck = Deck()):
        """
        Function that will initialise a new instance of Board.

        :param players: a list of players that will be playing at our Board
        """

        self.players = players
        self.turn_count = 0
        self.active_cards = []
        self.history_cards = []
        self.deck = deck

    def start_game(self):
        """
        Function that will start the game that we will be playing at our Board.
        """

        if self.deck.cards == []:
            self.deck.fill_deck_default()

        self.deck.shuffle()
        decks = self.deck.distribute(len(self.players))

        for index in range(len(self.players)):
            self.players[index].hand.cards = decks[str(index)]

        self.history_cards = decks["deck"]

        while len(self.players[0].hand.cards) > 0:
            self.history_cards += self.active_cards
            self.active_cards = []
            self.turn_count += 1

            for current_player in self.players:
                self.active_cards.append(current_player.play())

            print(self)

    def __str__(self) -> str:
        """
        Function that will return a printable version of our Board.

        :return: A str that will represent our current Board-state. Displaying
                    the current turn, what Cards are currently in play and how many Cards
                    have been played during the current game
        """

        return f"Turn {self.turn_count}: currently {[card.__str__() for card in self.active_cards]} are in the game and {len(self.history_cards)} cards have been played in earlier turns\n"


class UnoBoard(Board):
    def __init__(self, players: List[Player]):
        self.active_card = None
        self.order = 1
        self.deck = Deck()

        self.deck.cards = [
            UnoCard(card.card_type, card.value)
            for card in Deck.create_deck(
                ["red", "green", "yellow", "blue"],
                [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "+2",
                    "Reverse turn order",
                    "Skip turn",
                ],
                [Card("Special", "+4"), Card("Special", "Change color")],
            )
        ]
        super().__init__(players, self.deck)

    def start_game(self):

        self.deck.shuffle()
        decks = self.deck.distribute(len(self.players), 7)

        shuffle(self.players)
        active_player = 0

        for index in range(len(self.players)):
            self.players[index].hand.cards = decks[str(index)]

        while True:
            sleep(0.5)
            self.turn_count += 1
            while active_player >= len(self.players):
                active_player -= len(self.players)
            while active_player < 0:
                active_player += len(self.players)

            player = self.players[active_player]
            print(
                f"\nTurn {self.turn_count}: {player.name} is on the play with {len(player.hand.cards)} cards in hand."
            )
            if self.active_card is not None:
                print(f"The active card is {self.active_card}")

            player.legal_plays.cards = [
                card
                for card in player.hand.cards
                if card.is_legal_play(self.active_card)
            ]

            if player.legal_plays.cards != []:
                self.active_card = player.play()
            else:
                print(f"{player.name} has no legal plays and draws a card.")
                player.hand.cards.append(self.deck.draw())
                active_player += self.order
                continue

            self.deck.cards.append(self.active_card)

            if self.active_card.value == "+2":
                if active_player + self.order < 0:
                    self.players[len(self.players) - 1].hand.cards.append(
                        self.deck.draw()
                    )
                    self.players[len(self.players) - 1].hand.cards.append(
                        self.deck.draw()
                    )
                    "Reverse turn order",
                elif active_player + self.order >= len(self.players):
                    self.players[0].hand.cards.append(self.deck.draw())
                    self.players[0].hand.cards.append(self.deck.draw())
                else:
                    self.players[active_player + self.order].hand.cards.append(
                        self.deck.draw()
                    )
                    self.players[active_player + self.order].hand.cards.append(
                        self.deck.draw()
                    )
            elif self.active_card.value == "Skip turn":
                active_player += self.order
            elif self.active_card.value == "Reverse turn order":
                self.order *= -1
            elif self.active_card.value == "+4":
                if active_player + self.order < 0:
                    self.players[len(self.players) - 1].hand.cards.append(
                        self.deck.draw()
                    )
                    self.players[len(self.players) - 1].hand.cards.append(
                        self.deck.draw()
                    )
                    self.players[len(self.players) - 1].hand.cards.append(
                        self.deck.draw()
                    )
                    self.players[len(self.players) - 1].hand.cards.append(
                        self.deck.draw()
                    )
                    "Reverse turn order",
                elif active_player + self.order >= len(self.players):
                    self.players[0].hand.cards.append(self.deck.draw())
                    self.players[0].hand.cards.append(self.deck.draw())
                    self.players[0].hand.cards.append(self.deck.draw())
                    self.players[0].hand.cards.append(self.deck.draw())
                else:
                    self.players[active_player + self.order].hand.cards.append(
                        self.deck.draw()
                    )
                    self.players[active_player + self.order].hand.cards.append(
                        self.deck.draw()
                    )
                    self.players[active_player + self.order].hand.cards.append(
                        self.deck.draw()
                    )
                    self.players[active_player + self.order].hand.cards.append(
                        self.deck.draw()
                    )

                self.active_card = UnoCard(
                    choice(["red", "yellow", "green", "blue"]), "+4"
                )
            elif self.active_card.value == "Change color":
                self.active_card = UnoCard(
                    choice(["red", "yellow", "green", "blue"]), "Change color"
                )

            if len(player.hand.cards) == 1:
                print("Uno!")
            elif len(player.hand.cards) == 0:
                print(f"We have a winner!!! {player.name} wins the game!!!")
                break
            active_player += self.order
