import abc
from typing import TYPE_CHECKING, List

from mcts import interface

if TYPE_CHECKING:
    from mcts.state import State
    from mcts.custom_type import PlayerKey
    from mcts.move import Move


class Player(interface.Clonable, abc.ABC):
    """Define player."""

    @classmethod
    @abc.abstractmethod
    def possible_moves(cls, state: "State", player_key: "PlayerKey") -> List["Move"]:
        """
        Find all possible moves that a Player can make.

        Created moves should be independent of player instance because
        Moves will be executed on clone of player. So it's safer to get required player
        (self or enemy) by getting it from given state. This is a reason why this
        method id class method.

        :param state: current state of a game
        :param player_key: key for player declaring possible moves
        :return: list of all possible moves
        """
