import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import sympy as sp


@dataclass(frozen=True)
class BlockDiagram:
    nodes: list[str]
    edges: list[tuple[str, str, sp.Expr]]
    source: str
    sink: str


def _parse_edge(raw_edge: Iterable[str]) -> tuple[str, str, sp.Expr]:
    try:
        from_node, to_node, gain = raw_edge
    except (TypeError, ValueError) as exc:  # pragma: no cover - defensive for bad input shape
        raise ValueError(f"Edge must be [from, to, gain], got: {raw_edge}") from exc
    return str(from_node), str(to_node), sp.sympify(gain)


def parse_block_diagram(data: dict) -> BlockDiagram:
    required = {"nodes", "edges", "source", "sink"}
    missing = required.difference(data.keys())
    if missing:
        raise ValueError(f"Missing required fields: {sorted(missing)}")

    nodes = [str(n) for n in data["nodes"]]
    if not nodes:
        raise ValueError("nodes cannot be empty")

    edges = [_parse_edge(edge) for edge in data["edges"]]
    source = str(data["source"])
    sink = str(data["sink"])

    if source not in nodes:
        raise ValueError(f"source node '{source}' is not in nodes list")
    if sink not in nodes:
        raise ValueError(f"sink node '{sink}' is not in nodes list")

    for from_node, to_node, _ in edges:
        if from_node not in nodes or to_node not in nodes:
            raise ValueError(
                f"edge ({from_node} -> {to_node}) references a node not in nodes list"
            )

    return BlockDiagram(nodes=nodes, edges=edges, source=source, sink=sink)


def load_block_diagram_json(path: str | Path) -> BlockDiagram:
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return parse_block_diagram(data)
