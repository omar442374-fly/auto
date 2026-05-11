import unittest

import sympy as sp

from sfg_tool.block_diagram import parse_block_diagram
from sfg_tool.sfg_graph import build_sfg_graph


class TestSFGGraph(unittest.TestCase):
    def test_parallel_branches_are_summed(self) -> None:
        diagram = parse_block_diagram(
            {
                "nodes": ["a", "b"],
                "edges": [["a", "b", "G1"], ["a", "b", "G2"]],
                "source": "a",
                "sink": "b",
            }
        )
        graph = build_sfg_graph(diagram)
        self.assertEqual(sp.simplify(graph["a"]["b"]["gain"]), sp.sympify("G1 + G2"))


if __name__ == "__main__":
    unittest.main()

