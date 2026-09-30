#!/usr/bin/env python3
"""Validate TeSA descriptor JSON files for reproducibility."""

from __future__ import annotations

import json
from pathlib import Path


EXPECTED_CLASS_COUNTS = {
    "UCM": 21,
    "NWPU": 45,
    "AID": 30,
    "rsscn7": 7,
    "EuroSAT": 10,
}


def validate_file(path: Path, expected_classes: int) -> list[str]:
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{path}: invalid JSON: {exc}"]

    if not isinstance(payload, dict):
        return [f"{path}: root value must be an object"]
    if len(payload) != expected_classes:
        errors.append(
            f"{path}: expected {expected_classes} classes, found {len(payload)}"
        )

    for class_name, descriptors in payload.items():
        if not isinstance(class_name, str) or not class_name.strip():
            errors.append(f"{path}: invalid class name {class_name!r}")
        if not isinstance(descriptors, list):
            errors.append(f"{path}: {class_name}: descriptors must be a list")
            continue
        if len(descriptors) != 10:
            errors.append(
                f"{path}: {class_name}: expected 10 descriptors, found {len(descriptors)}"
            )
        normalized: list[str] = []
        for descriptor in descriptors:
            if not isinstance(descriptor, str) or not descriptor.strip():
                errors.append(f"{path}: {class_name}: empty/non-string descriptor")
                continue
            normalized.append(" ".join(descriptor.lower().split()))
        if len(normalized) != len(set(normalized)):
            errors.append(f"{path}: {class_name}: duplicate descriptors")
    return errors


def main() -> None:
    repository_root = Path(__file__).resolve().parents[1]
    descriptor_root = repository_root / "descriptors"
    generation_dirs = sorted(p for p in descriptor_root.iterdir() if p.is_dir())
    if not generation_dirs:
        raise SystemExit("No descriptor generation directories were found")

    errors: list[str] = []
    for generation_dir in generation_dirs:
        for dataset, expected_classes in EXPECTED_CLASS_COUNTS.items():
            path = generation_dir / f"{dataset}.json"
            if not path.exists():
                errors.append(f"{path}: missing file")
                continue
            errors.extend(validate_file(path, expected_classes))

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(
        f"Validation passed: {len(generation_dirs)} generations, "
        f"{len(EXPECTED_CLASS_COUNTS)} datasets, 10 descriptors per class."
    )


if __name__ == "__main__":
    main()
