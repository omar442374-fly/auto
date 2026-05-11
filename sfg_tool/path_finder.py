from itertools import combinations

import networkx as nx
import sympy as sp


def path_gain(graph: nx.DiGraph, path: list[str]) -> sp.Expr:
    gain = sp.Integer(1)
    for i in range(len(path) - 1):
        gain *= graph[path[i]][path[i + 1]]["gain"]
    return sp.simplify(gain)


def loop_gain(graph: nx.DiGraph, loop: list[str]) -> sp.Expr:
    gain = sp.Integer(1)
    for i in range(len(loop)):
        gain *= graph[loop[i]][loop[(i + 1) % len(loop)]]["gain"]
    return sp.simplify(gain)


def find_forward_paths(graph: nx.DiGraph, source: str, sink: str) -> list[list[str]]:
    if source not in graph or sink not in graph:
        return []
    return [list(path) for path in nx.all_simple_paths(graph, source, sink)]


def find_loops(graph: nx.DiGraph) -> list[list[str]]:
    return [list(cycle) for cycle in nx.simple_cycles(graph)]


def loops_are_non_touching(loop_a: list[str], loop_b: list[str]) -> bool:
    return set(loop_a).isdisjoint(loop_b)


def find_non_touching_loop_groups(
    loops: list[list[str]], group_size: int
) -> list[tuple[list[str], ...]]:
    groups: list[tuple[list[str], ...]] = []
    for candidate in combinations(loops, group_size):
        all_non_touching = True
        for i in range(len(candidate)):
            for j in range(i + 1, len(candidate)):
                if not loops_are_non_touching(candidate[i], candidate[j]):
                    all_non_touching = False
                    break
            if not all_non_touching:
                break
        if all_non_touching:
            groups.append(candidate)
    return groups
