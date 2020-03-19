import itertools
from collections import defaultdict

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
        """
        Initialize state.

        :param players: map players identifier to players
        """
        self.players = players

        self.final = False
        self.win_stats: Dict["PlayerKey", int] = defaultdict(int)
        self._next_states: Dict["Move", "State"] = None

        self.id_nr = self._nr
        State._nr += 1

    @property
    def next_states(self) -> Dict["Move", "State"]:
        if self._next_states is None:
            self._next_states = {move: None for move in self.find_next_moves()}
            if not self._next_states:
                self.final = True

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

    def execute_one_move(self, quick=False) -> "PlayerKey":
        """
        Explore tree.

        Pick one move with based of knowledge (but slow) and simulate rest of game at random (but quick).

        :return: winner of game
        """
        if not self.next_states:
            self.final = True
            winner = self.pick_winner()
            self.win_stats[winner] += 1
            return winner

        move = self.pick_move(quick)

        next_state = self.next_states[move]
        if next_state is None:
            next_state = move.execute()
            self.next_states[move] = next_state

        winner = next_state.execute_one_move(quick=True)
        self.win_stats[winner] += 1
        return winner

    def pick_move(self, quick=True) -> "Move":
        if quick:
            return random.choice(list(self.next_states.keys()))
        else:
            # TODO picking move should be more sophisticated.
            # TODO Took to account win ratio and number of picking this move before
            return random.choice(list(self.next_states.keys()))

    @abc.abstractmethod
    def pick_winner(self) -> "PlayerKey":
        """
        Pick winner from given state.
        :return: winner
        """

    def clone(self) -> "State":
        """
        Create deep clone of self.

        :return: clone of self.
        """
        return self.__class__(
            players={
                player_key: player.clone()
                for player_key, player in self.players.items()
            }
        )
