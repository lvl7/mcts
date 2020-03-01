import itertools

import random
from functools import partial
from typing import List

from mcts import interface
from mcts import player
from mcts.custom_type import PlayerKey
from mcts.ilustrate import draw_tree
from mcts.move import Move
from mcts.state import State


class Card(interface.Clonable):
    def __init__(self, type, number):
        self.type = type
        self.number = number

    def clone(self) -> "Card":
        return Card(self.type, self.number)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return NotImplemented

        return all([
            self.type == other.type,
            self.number == other.number,
        ])


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

    def end_turn(self, state: "State"):
        self.active = False

    def next_player(self, state: "State"):
        next_player_name = player_names[(player_names.index(self.name) + 1) % len(player_names)]
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
                consequences=[
                    player.end_turn,
                    player.next_player,
                ]
            )
            for card in player.hand
        ]

    def clone(self) -> "Player":
        return Player(
            name=self.name,
            hand=[card.clone() for card in self.hand],
            active=self.active
        )


if __name__ == "__main__":
    deck = Player(
        name="DECK",
        hand=[
            Card(type=card_type, number=number)
            for card_type, number in itertools.product("ABC", range(3))
        ],
        active=False,
    )
    random.shuffle(deck.hand)

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

    list(players.values())[0].active = True
    players["BOARD"] = Player("BOARD", [], active=False)
    players[deck.name] = deck

    state = State(
        players=players,
    )

    state.execute_one_move()
    state.execute_one_move()
    state.execute_one_move()
    state.execute_one_move()
    state.execute_one_move()
    state.execute_one_move()

    draw_tree.draw(state)
