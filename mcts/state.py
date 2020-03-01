import itertools

import abc
import random
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from mcts.custom_type import PlayerKey
    from mcts.player import Player
    from mcts.move import Move


class State(abc.ABC):
    """
    Describe moment of a game.

    Keep information about one particle state of a game.
    Keep track of possible moves that leads to other states.
    """

    _nr = 0

    def __init__(self, players: Dict["PlayerKey", "Player"]):
        self.players = players

        self.final = False
        self._next_states: Dict["Move", "State"] = None

        self.id_nr = self._nr
        State._nr += 1

    @property
    def next_states(self) -> Dict["Move", "State"]:
        if self._next_states is None:
            self._next_states = {move: None for move in self.find_next_moves()}

        return self._next_states

    def find_next_moves(self):
        """
        Collect all possible moves from each player.

        Keep them in ``self.moves``
        """
        return list(
            itertools.chain(
                *(player.clone().possible_moves(self, player_key) for player_key, player in self.players.items())
            )
        )

    def execute_one_move(self):
        # TODO picking move should be more sophisticated.
        # TODO Took to account win ratio and number of picking this move before

        move = random.choice(list(self.next_states))
        next_step = self.next_states[move]

        if next_step is None:
            next_step = move.execute()
            self.next_states[move] = next_step

    def clone(self) -> "State":
        """
        Create deep clone of self.

        :return: clone of self.
        """
        return State(
            players={
                player_key: player.clone()
                for player_key, player in self.players.items()
            }
        )
