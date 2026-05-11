# Signal Flow Graph (SFG) Tool

Simple Python project for:
1. Building a Signal Flow Graph (SFG) from a JSON block diagram format.
2. Finding forward paths and loops.
3. Computing overall transfer function using Mason's Gain Formula.

## Folder Structure

```
project_root/
├── sfg_tool/
│   ├── __init__.py
│   ├── block_diagram.py
│   ├── sfg_graph.py
│   ├── path_finder.py
│   ├── mason.py
│   ├── visualizer.py
│   ├── gui.py
│   └── main.py
├── examples/
│   ├── example1.json
│   └── example2.json
└── tests/
    ├── test_sfg_graph.py
    ├── test_path_finder.py
    └── test_mason.py
```

## Install

```bash
pip install networkx matplotlib sympy
```

## Run CLI

```bash
cd project_root
python3 -m sfg_tool.main --input examples/example1.json
```

Save graph image:

```bash
python3 -m sfg_tool.main \
  --input examples/example1.json \
  --save-figure examples/example1.png
```

## Run GUI (optional)

```bash
python3 -c "from sfg_tool.gui import run_gui; run_gui()"
```

## Run Tests

```bash
cd project_root
python3 -m unittest discover -s tests -q
```
