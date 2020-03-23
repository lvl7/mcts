from typing import TYPE_CHECKING, Callable, List

if TYPE_CHECKING:
    from mcts.state import State
    from mcts.custom_type import PlayerKey


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
            player_in_move_key: "PlayerKey",
            action: Callable[["State"], None],
            description: str,
            consequences: List[Callable[["State"], None]]
    ):
        """
        Initialize move.

        :param state_from: state from where move begins
        :param player_in_move_key: key for getting player from state
        :param action: action defining move - should define only one action - like playing a card
        :param description: short description of move - like `Player1 plays K4`
        :param consequences: list of consequences after ``action`` - like adding score; redraw card; end turn
        """
        # TODO make sure that each of consequences is class methods as well
        #      (need to NOT modify player - action and consequences will be used on clones of caster)
        self.player_in_move_key = player_in_move_key
        self.state_from = state_from
        self.action = action
        self.consequences = consequences
        self.description = description

    def execute(self) -> "State":
        """
        Create state by executing action and each of consequences on a copy of ``state_from``.

        :returns: new state
        """

        state = self.state_from.clone()
        self.action(state)
        for consequence in self.consequences:
            consequence(state)

        return state

    def __str__(self):
        return self.description
