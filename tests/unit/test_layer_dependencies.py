"""Katman kuralı: bir paket yalnızca kendinden alttaki katmanları içe aktarabilir."""

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAYERS = {"utils": 0, "config": 1, "philosophers": 2, "safety": 2, "services": 3, "llm": 4, "ui": 5}


def _imports(path: Path):
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            yield from (a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            yield node.module.split(".")[0]


def test_no_upward_or_sideways_imports():
    violations = []
    for pkg, layer in LAYERS.items():
        for f in (ROOT / pkg).rglob("*.py"):
            for imp in set(_imports(f)) & LAYERS.keys():
                if imp != pkg and LAYERS[imp] >= layer:
                    violations.append(f"{f.relative_to(ROOT)} → {imp}")
    assert not violations, violations
