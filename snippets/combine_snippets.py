"""Combine VS Code snippet JSON files into one.

- Supports snippet files containing `//` comment lines and trailing commas by
  using `ast.literal_eval` after stripping line comments.
- Writes a combined JSON file with all snippet entries.
- Logs duplicate snippet keys.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

COMMENT_LINE = re.compile(r"^\s*//")


def strip_line_comments(text: str) -> str:
    """Remove full-line // comments while keeping content unchanged."""
    lines: List[str] = []
    for line in text.splitlines():
        if COMMENT_LINE.match(line):
            continue
        lines.append(line)
    return "\n".join(lines)


def load_snippet_file(path: Path) -> Dict:
    cleaned = strip_line_comments(path.read_text(encoding="utf-8"))
    try:
        data = ast.literal_eval(cleaned)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to parse {path.name}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"Snippet file {path} did not contain a top-level dict")
    return data


def merge_snippets(files: List[Path]) -> Tuple[Dict, Dict[str, List[str]]]:
    combined: Dict = {}
    collisions: Dict[str, List[str]] = {}
    for path in files:
        data = load_snippet_file(path)
        for key, val in data.items():
            if key in combined:
                collisions.setdefault(key, []).append(path.name)
            combined[key] = val
    return combined, collisions


def write_snippets(path: Path, snippets: Dict) -> None:
    path.write_text(
        json.dumps(snippets, indent=4, ensure_ascii=False), encoding="utf-8"
    )


def compare_dicts(a: Dict, b: Dict) -> Tuple[List[str], List[str], List[str]]:
    """Return (only_in_a, only_in_b, different_values_keys)."""
    keys_a = set(a.keys())
    keys_b = set(b.keys())
    only_a = sorted(keys_a - keys_b)
    only_b = sorted(keys_b - keys_a)
    shared = keys_a & keys_b
    different = sorted(k for k in shared if a[k] != b[k])
    return only_a, only_b, different


def main(
    output_name: str = "snippets_all_combined.json",
    reference_name: str = "snippets_all.json",
    update_reference: bool = True,
) -> None:
    base = Path(__file__).parent
    files = sorted(
        p
        for p in base.glob("*.json")
        if p.name != output_name and not p.stem.startswith("snippets_all")
    )
    if not files:
        raise SystemExit("No snippet files found.")

    combined, collisions = merge_snippets(files)
    out_path = base / output_name
    write_snippets(out_path, combined)

    print(f"Wrote {len(combined)} snippets to {out_path}")
    if collisions:
        print("Duplicate snippet keys (last wins):")
        for key, origins in collisions.items():
            print(f"  {key}: {origins}")

    ref_path = base / reference_name
    if ref_path.exists():
        reference = load_snippet_file(ref_path)
        only_combined, only_ref, different = compare_dicts(combined, reference)
        if not (only_combined or only_ref or different):
            print(f"Reference {reference_name} matches the combined output.")
        else:
            print("Reference mismatch detected:")
            if only_combined:
                print(f"  Missing in reference ({len(only_combined)}): {only_combined}")
            if only_ref:
                print(f"  Missing in combined ({len(only_ref)}): {only_ref}")
            if different:
                print(f"  Different values ({len(different)} keys): {different}")
            if update_reference:
                write_snippets(ref_path, combined)
                print(f"Reference {reference_name} updated to match combined output.")
    else:
        write_snippets(ref_path, combined)
        print(f"Reference {reference_name} created.")


if __name__ == "__main__":
    main()
