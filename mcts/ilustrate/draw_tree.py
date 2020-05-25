from colorsys import hsv_to_rgb

import pygraphviz as gz
from typing import TYPE_CHECKING, Dict

from mcts.player import Player

if TYPE_CHECKING:
    from mcts.state import State
    from mcts.custom_type import PlayerKey


def _get_player_description(player: "Player"):
    return "|".join(
        (f"{card.type}{card.number}" for card in player.hand)
    )


def _get_players_description(players, win_stats: Dict["PlayerKey", int]):
    return "|".join(
        f"""
            {{ 
                {win_stats[name]}:{name}"
                |{{
                    {_get_player_description(player)} 
                }} 
            }}
        """
        for name, player in players.items()
    )


def _state_win_ratio(win_stats: Dict[str, int]):
    return "|".join(
        f"{{ {name} | {wins} }}"
        for name, wins in win_stats.items()
    )


def _state_to_node(state: "State"):
    return f"""
        {{
            {{
                {state.id_nr}|{state.final}
            }}
            |{_get_players_description(state.players, state.win_stats)}
        }}
    """

def _pick_color(state: "State"):
    most_winning_player, player_wins = sorted(
        state.win_stats.items(),
        key=lambda player_stats: player_stats[0],
        reverse=True,
    )[0]

    wins = sum(state.win_stats.values())

    players = len(state.players)
    player_no = list(state.players.keys()).index(most_winning_player)

    color_tuple = hsv_to_rgb(player_no / players, player_wins / wins, 1)

    colors_int = list(int(c * 255) for c in color_tuple)
    hex_colors = list(f"{color:0>2X}" for color in colors_int)
    color = "#" + "".join(hex_colors)

    return color


def _construct_graph(graph: gz.AGraph, state):
    graph.add_node(
        state.id_nr,
        label=_state_to_node(state),
        shape="record",
        style="filled",
        fillcolor=_pick_color(state),
    )

    for move, next_state in state.next_states.items():
        if next_state:
            _construct_graph(graph, next_state)
            graph.add_edge(
                u=state.id_nr,
                v=next_state.id_nr,
                key="l",
                label=str(move)
            )


def draw(state: "State"):
    graph = gz.AGraph(overlap="prism")

    _construct_graph(graph, state)

    graph.layout("dot")
    graph.write("g.dot")
    graph.draw("g.png")
