"""Pytest-style test to validate snippet combining on dummy fixtures."""

import sys
from pathlib import Path

# Ensure project snippets module is importable when running from this folder
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from combine_snippets import (
    compare_dicts,
    load_snippet_file,  # type: ignore
    merge_snippets,
    write_snippets,
)


def test_combine_snippets(tmp_path: Path) -> None:
    base = Path(__file__).parent
    files = sorted(
        p
        for p in base.glob("snippets_*.json")
        if p.name in {"snippets_a.json", "snippets_b.json"}
    )
    combined, collisions = merge_snippets(files)

    expected = load_snippet_file(base / "expected_combined.json")
    only_combined, only_expected, different = compare_dicts(combined, expected)

    assert not only_combined, f"Unexpected keys: {only_combined}"
    assert not only_expected, f"Missing keys: {only_expected}"
    assert not different, f"Different values for keys: {different}"

    assert collisions == {
        "foo": ["snippets_b.json"]
    }, f"Unexpected collisions: {collisions}"

    out_path = tmp_path / "combined_test_output.json"
    write_snippets(out_path, combined)
