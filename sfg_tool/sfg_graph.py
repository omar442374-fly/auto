import networkx as nx
import sympy as sp

from .block_diagram import BlockDiagram


class SFGGraph:
    def __init__(self) -> None:
        self._graph = nx.DiGraph()

    def add_node(self, node: str) -> None:
        self._graph.add_node(node)

    def add_branch(self, from_node: str, to_node: str, gain: sp.Expr) -> None:
        if self._graph.has_edge(from_node, to_node):
            current_gain = self._graph[from_node][to_node]["gain"]
            self._graph[from_node][to_node]["gain"] = sp.simplify(current_gain + gain)
            return
        self._graph.add_edge(from_node, to_node, gain=sp.sympify(gain))

    def get_graph(self) -> nx.DiGraph:
        return self._graph


def build_sfg_graph(diagram: BlockDiagram) -> nx.DiGraph:
    sfg = SFGGraph()
    for node in diagram.nodes:
        sfg.add_node(node)
    for from_node, to_node, gain in diagram.edges:
        sfg.add_branch(from_node, to_node, gain)
    return sfg.get_graph()
