from itertools import combinations

import networkx as nx
import sympy as sp

from .path_finder import (
    find_forward_paths,
    find_loops,
    loop_gain,
    loops_are_non_touching,
    path_gain,
)


def _compute_delta(graph: nx.DiGraph, loops: list[list[str]]) -> sp.Expr:
    if not loops:
        return sp.Integer(1)

    delta = sp.Integer(1)

    loop_gain_map = {tuple(loop): loop_gain(graph, loop) for loop in loops}

    for k in range(1, len(loops) + 1):
        combo_sum = sp.Integer(0)
        for combo in combinations(loops, k):
            valid = True
            for i in range(len(combo)):
                for j in range(i + 1, len(combo)):
                    if not loops_are_non_touching(combo[i], combo[j]):
                        valid = False
                        break
                if not valid:
                    break
            if not valid:
                continue

            product = sp.Integer(1)
            for loop in combo:
                product *= loop_gain_map[tuple(loop)]
            combo_sum += product

        if combo_sum == 0:
            continue

        if k % 2 == 1:
            delta -= combo_sum
        else:
            delta += combo_sum

    return sp.simplify(delta)


def _loop_touches_path(loop_nodes: list[str], path_nodes: list[str]) -> bool:
    return not set(loop_nodes).isdisjoint(path_nodes)


def compute_mason_transfer_function(
    graph: nx.DiGraph, source: str, sink: str
) -> dict[str, object]:
    forward_paths = find_forward_paths(graph, source, sink)
    loops = find_loops(graph)

    if not forward_paths:
        return {
            "forward_paths": [],
            "path_gains": [],
            "loops": loops,
            "loop_gains": [loop_gain(graph, loop) for loop in loops],
            "delta": _compute_delta(graph, loops),
            "path_deltas": [],
            "transfer_function": sp.Integer(0),
        }

    path_gains = [path_gain(graph, p) for p in forward_paths]
    loop_gains = [loop_gain(graph, l) for l in loops]
    delta = _compute_delta(graph, loops)

    if sp.simplify(delta) == 0:
        raise ValueError("Graph determinant Δ is zero; transfer function is undefined.")

    numerator = sp.Integer(0)
    path_deltas: list[sp.Expr] = []
    for p, p_gain in zip(forward_paths, path_gains):
        path_non_touching_loops = [loop for loop in loops if not _loop_touches_path(loop, p)]
        delta_k = _compute_delta(graph, path_non_touching_loops)
        path_deltas.append(delta_k)
        numerator += p_gain * delta_k

    transfer_function = sp.cancel(sp.simplify(numerator / delta))

    return {
        "forward_paths": forward_paths,
        "path_gains": path_gains,
        "loops": loops,
        "loop_gains": loop_gains,
        "delta": delta,
        "path_deltas": path_deltas,
        "transfer_function": transfer_function,
    }

