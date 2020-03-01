from typing import TYPE_CHECKING, Callable, List

if TYPE_CHECKING:
    from mcts.state import State


class Move:
    """
    Lead from one ``State`` to another.

    Should be defined as:
        - ony one action
        - collection of consequences

    ``Move`` will create copy of given state and apply ``action`` and ``consequences`` to model
    how result (after move) state will look like.

    Example:
        action: play a third card (defined as function which move card from player and add it to
                environment player board)
        consequences: gain 3 point; draw card; decrease possible moves this turn by one.
    """

    def __init__(
            self,
            state_from: "State",
            player_in_move_name: str,
            action: Callable[["State"], None],
            consequences: List[Callable[["State"], None]]
    ):
        self.player_in_move_name = player_in_move_name
        self.state_from = state_from
        self.action = action
        self.consequences = consequences

    def execute(self) -> "State":
        """
        Create state be executing action and each of consequences on a copy of ``state_from``.

        :returns: new state
        """

        state = self.state_from.clone()
        self.action(state)
        for consequence in self.consequences:
            consequence(state)

        return state
