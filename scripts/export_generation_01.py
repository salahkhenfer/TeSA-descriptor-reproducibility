#!/usr/bin/env python3
"""Export TAXONOMIES_RAW from a TeSA Python source file without importing it."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path


# These two legacy entries exist in TAXONOMIES_RAW but are not NWPU-RESISC45
# dataset classes and are never indexed by the evaluation loader.
UNUSED_SOURCE_KEYS = {"NWPU": {"residential", "woodland"}}


def load_taxonomies(source_path: Path) -> dict:
    module = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "TAXONOMIES_RAW":
                    value = ast.literal_eval(node.value)
                    if not isinstance(value, dict):
                        raise TypeError("TAXONOMIES_RAW is not a dictionary")
                    return value
    raise KeyError("TAXONOMIES_RAW was not found")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Path to tesa_ablations.py")
    parser.add_argument("output", type=Path, help="Output generation directory")
    args = parser.parse_args()

    taxonomies = load_taxonomies(args.source)
    args.output.mkdir(parents=True, exist_ok=True)
    for dataset, classes in taxonomies.items():
        unused_keys = UNUSED_SOURCE_KEYS.get(dataset, set())
        classes = {
            class_name: descriptors
            for class_name, descriptors in classes.items()
            if class_name not in unused_keys
        }
        output_path = args.output / f"{dataset}.json"
        output_path.write_text(
            json.dumps(classes, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
