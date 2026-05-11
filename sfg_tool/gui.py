import json
import tkinter as tk
from tkinter import filedialog, messagebox

from .block_diagram import parse_block_diagram
from .mason import compute_mason_transfer_function
from .sfg_graph import build_sfg_graph


class SFGGui(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("SFG Tool (Simple)")
        self.geometry("900x600")

        self.input_text = tk.Text(self, height=18, width=120)
        self.input_text.pack(padx=10, pady=10, fill=tk.BOTH)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Load JSON", command=self.load_json).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(button_frame, text="Compute", command=self.compute).pack(
            side=tk.LEFT, padx=5
        )

        self.output_text = tk.Text(self, height=15, width=120)
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def load_json(self) -> None:
        path = filedialog.askopenfilename(
            title="Select input JSON", filetypes=[("JSON files", "*.json")]
        )
        if not path:
            return
        with open(path, "r", encoding="utf-8") as file:
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert(tk.END, file.read())

    def compute(self) -> None:
        try:
            payload = json.loads(self.input_text.get("1.0", tk.END))
            diagram = parse_block_diagram(payload)
            graph = build_sfg_graph(diagram)
            result = compute_mason_transfer_function(graph, diagram.source, diagram.sink)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(
                tk.END, f"Transfer Function:\n{result['transfer_function']}\n\n"
            )
            self.output_text.insert(tk.END, f"Δ = {result['delta']}\n")
            self.output_text.insert(tk.END, "\nForward Paths:\n")
            for i, (p, g) in enumerate(
                zip(result["forward_paths"], result["path_gains"]), start=1
            ):
                self.output_text.insert(tk.END, f"P{i}: {' -> '.join(p)} | gain={g}\n")
            self.output_text.insert(tk.END, "\nLoops:\n")
            for i, (l, g) in enumerate(zip(result["loops"], result["loop_gains"]), start=1):
                self.output_text.insert(tk.END, f"L{i}: {' -> '.join(l)} -> {l[0]} | gain={g}\n")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))


def run_gui() -> None:
    app = SFGGui()
    app.mainloop()
