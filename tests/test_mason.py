import unittest

import sympy as sp

from sfg_tool.block_diagram import parse_block_diagram
from sfg_tool.mason import compute_mason_transfer_function
from sfg_tool.sfg_graph import build_sfg_graph


class TestMason(unittest.TestCase):
    def test_example2_transfer_function(self) -> None:
        diagram = parse_block_diagram(
            {
                "nodes": ["r", "e", "x", "c"],
                "edges": [
                    ["r", "e", "1"],
                    ["e", "x", "G1"],
                    ["x", "c", "G2"],
                    ["c", "e", "-H1"],
                    ["c", "x", "-H2"],
                ],
                "source": "r",
                "sink": "c",
            }
        )
        graph = build_sfg_graph(diagram)
        result = compute_mason_transfer_function(graph, "r", "c")

        expected = sp.sympify("G1*G2/(1 + G2*H2 + G1*G2*H1)")
        self.assertEqual(sp.simplify(result["transfer_function"] - expected), 0)

    def test_no_forward_path_returns_zero(self) -> None:
        diagram = parse_block_diagram(
            {
                "nodes": ["a", "b", "c"],
                "edges": [["a", "b", "1"]],
                "source": "a",
                "sink": "c",
            }
        )
        graph = build_sfg_graph(diagram)
        result = compute_mason_transfer_function(graph, "a", "c")
        self.assertEqual(result["transfer_function"], 0)


if __name__ == "__main__":
    unittest.main()
