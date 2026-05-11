import unittest

import sympy as sp

from sfg_tool.block_diagram import parse_block_diagram
from sfg_tool.path_finder import (
    find_forward_paths,
    find_loops,
    find_non_touching_loop_groups,
    path_gain,
)
from sfg_tool.sfg_graph import build_sfg_graph


class TestPathFinder(unittest.TestCase):
    def test_forward_paths_and_loops(self) -> None:
        diagram = parse_block_diagram(
            {
                "nodes": ["x1", "x2", "x3", "x4", "x5"],
                "edges": [
                    ["x1", "x2", "1"],
                    ["x2", "x3", "G1"],
                    ["x3", "x4", "G2"],
                    ["x4", "x5", "1"],
                    ["x4", "x2", "-H1"],
                    ["x5", "x3", "-H2"],
                ],
                "source": "x1",
                "sink": "x5",
            }
        )
        graph = build_sfg_graph(diagram)

        forward_paths = find_forward_paths(graph, "x1", "x5")
        self.assertEqual(forward_paths, [["x1", "x2", "x3", "x4", "x5"]])
        self.assertEqual(path_gain(graph, forward_paths[0]), sp.sympify("G1*G2"))

        loops = find_loops(graph)
        self.assertEqual(len(loops), 2)

        non_touching_pairs = find_non_touching_loop_groups(loops, 2)
        self.assertEqual(non_touching_pairs, [])


if __name__ == "__main__":
    unittest.main()

