import argparse

from .block_diagram import load_block_diagram_json
from .mason import compute_mason_transfer_function
from .sfg_graph import build_sfg_graph
from .visualizer import draw_sfg


def _print_result(result: dict[str, object]) -> None:
    print("Forward Paths:")
    for i, (path, gain) in enumerate(
        zip(result["forward_paths"], result["path_gains"]), start=1
    ):
        print(f"  P{i}: {' -> '.join(path)} | Gain: {gain}")

    print("\nLoops:")
    for i, (loop, gain) in enumerate(zip(result["loops"], result["loop_gains"]), start=1):
        print(f"  L{i}: {' -> '.join(loop)} -> {loop[0]} | Gain: {gain}")

    print(f"\nΔ (Graph Determinant): {result['delta']}")
    for i, delta_k in enumerate(result["path_deltas"], start=1):
        print(f"Δ{i}: {delta_k}")

    print(f"\nTransfer Function: {result['transfer_function']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute transfer function from SFG using Mason's Gain Formula."
    )
    parser.add_argument("--input", required=True, help="Path to input JSON file")
    parser.add_argument("--save-figure", default=None, help="Optional output image path")
    parser.add_argument(
        "--show-figure", action="store_true", help="Show graph window using Matplotlib"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    diagram = load_block_diagram_json(args.input)
    graph = build_sfg_graph(diagram)
    result = compute_mason_transfer_function(graph, diagram.source, diagram.sink)
    _print_result(result)

    if args.save_figure or args.show_figure:
        draw_sfg(
            graph,
            title="Signal Flow Graph",
            save_path=args.save_figure,
            show=args.show_figure,
        )


if __name__ == "__main__":
    main()
