"""Simplified card game

# items:
Deck is composed with cards with two characteristics:
 - symbol (A, B, C)
 - number (1, 2, 3)

# preparation:
 - shuffle deck
 - each player gets two cards

# Rules:
- Goal is to have empty hand after turn end

# Turns:
- player play card from hand
- if played card symbol or number match last played card, player get two cards below played
- check win condition

"""

import itertools

import random
from functools import partial
from typing import List, Dict, Optional

from mcts import interface, state
from mcts import player
from mcts.custom_type import PlayerKey
from mcts.ilustrate import draw_tree
from mcts.move import Move


class Card(interface.Clonable):
    def __init__(self, type, number):
        self.type = type
        self.number = number

    def clone(self) -> "Card":
        return self.__class__(self.type, self.number)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return NotImplemented

        return all([
            self.type == other.type,
            self.number == other.number,
        ])

    def __str__(self):
        return f"{self.type}{self.number}"


player_names = ["P1", "P2", "P3"]


class Player(player.Player):
    def __init__(self, name, hand: List[Card], active: bool):
        self.name = name
        self.hand = hand
        self.active = active

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return NotImplemented

        return all([
            self.name == other.name,
            self.hand == other.hand,
            self.active == other.active,
        ])

    @classmethod
    def play_card(cls, state: "State", caster_key: "PlayerKey", card: "Card"):
        caster = state.players[caster_key]

        caster.hand.remove(card)
        state.players["BOARD"].hand.append(card)

    @classmethod
    def end_turn(cls, state: "State", caster_key: "PlayerKey"):
        caster = state.players[caster_key]
        caster.active = False

    @classmethod
    def resolve_played_card(cls, state: "State", caster_key: "PlayerKey"):
        caster: "Player" = state.players[caster_key]
        board: "Player" = state.players["BOARD"]

        last_played_cards = board.hand[-3:]
        if len(last_played_cards) <= 1:
            return

        if (last_played_cards[-1].type == last_played_cards[-2].type
            or last_played_cards[-1].number == last_played_cards[-2].number
            ):

            for card_to_draw in last_played_cards[:-1]:
                caster.hand.append(card_to_draw)
                board.hand.remove(card_to_draw)

    @classmethod
    def next_player(cls, state: "State", caster_key: "PlayerKey"):
        next_player_name = player_names[(player_names.index(caster_key) + 1) % len(player_names)]
        state.players[next_player_name].active = True

    @classmethod
    def possible_moves(cls, state: "State", player_key: "PlayerKey") -> List["Move"]:
        player = state.players[player_key]
        if not player.active:
            return []

        return [
            Move(
                state_from=state,
                player_in_move_key=player.name,
                action=partial(Player.play_card, caster_key=player_key, card=card),
                description=f"{player.name}:{card}",
                consequences=[
                    partial(Player.end_turn, caster_key=player_key),
                    partial(Player.resolve_played_card, caster_key=player_key),
                    partial(Player.next_player, caster_key=player_key),
                ]
            )
            for card in player.hand
        ]

    def clone(self) -> "Player":
        return self.__class__(
            name=self.name,
            hand=[card.clone() for card in self.hand],
            active=self.active
        )


class State(state.State):
    def pick_winner(self) -> Optional["PlayerKey"]:
        """
        Pick random winner.

        Prefer player 0, then 1, then 2 ...

        :return: winner
        """
        for player_name, player in self.players.items():
            if player_name not in player_names:
                continue

            if not player.hand:
                return player_name


def init_deck() -> "Player":
    deck = Player(
        name="DECK",
        hand=[
            Card(type=card_type, number=number)
            for card_type, number in itertools.product("ABC", range(3))
        ],
        active=False,
    )
    random.shuffle(deck.hand)

    return deck


def init_players(deck: "Player") -> Dict[str, "Player"]:
    players = {}

    for player_name in player_names:
        players[player_name] = Player(
            name=player_name,
            hand=[
                deck.hand.pop(),
                deck.hand.pop(),
            ],
            active=False,
        )

    return players


def init_board() -> "Player":
    return Player("BOARD", [], active=False)


def execute_game(state: "State"):
    for i in range(100):
        state.execute_one_move()

    draw_tree.draw(state)


def main():
    deck = init_deck()
    board = init_board()
    players = init_players(deck)

    list(players.values())[0].active = True

    players[board.name] = board
    players[deck.name] = deck

    state = State(
        players=players,
    )

    execute_game(state)


if __name__ == "__main__":
    main()
