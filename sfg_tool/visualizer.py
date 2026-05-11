from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx


def draw_sfg(
    graph: nx.DiGraph,
    title: str = "Signal Flow Graph",
    save_path: str | None = None,
    show: bool = False,
) -> None:
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(graph, seed=42)

    nx.draw_networkx_nodes(graph, pos, node_size=1200, node_color="#dbeafe")
    nx.draw_networkx_labels(graph, pos, font_size=10)
    nx.draw_networkx_edges(graph, pos, arrows=True, arrowsize=20, edge_color="#334155")

    edge_labels = {(u, v): str(data.get("gain", "")) for u, v, data in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=9)

    plt.title(title)
    plt.axis("off")
    plt.tight_layout()

    if save_path:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(path, dpi=200)

    if show:
        plt.show()

    plt.close()

