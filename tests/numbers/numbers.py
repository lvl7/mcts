from typing import List

from mcts import player
from mcts import state as mcts_state
from mcts.move import Move


class Player(player.Player):
    def __init__(self):
        self.hand = []

    def clone(self) -> "Player":
        clone = Player()
        clone.hand = [card.clone() for card in self.hand]

        return clone

    def possible_moves(self, state: "mcts_state.State") -> List[Move]:
        pass


if __name__ == "__main__":
    players = [Player() for _ in range(3)]

    c_state = mcts_state.State(players)
    c_state.find_next_moves()
