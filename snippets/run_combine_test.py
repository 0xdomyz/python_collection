"""Small test to validate snippet combining on dummy fixtures."""

from pathlib import Path

from combine_snippets import (
    compare_dicts,
    load_snippet_file,
    merge_snippets,
    write_snippets,
)


def run_test() -> None:
    base = Path(__file__).parent / "test_snippets"
    files = sorted(p for p in base.glob("*.json") if p.name != "expected_combined.json")
    combined, collisions = merge_snippets(files)

    expected = load_snippet_file(base / "expected_combined.json")
    only_combined, only_expected, different = compare_dicts(combined, expected)

    assert not only_combined, f"Unexpected keys: {only_combined}"
    assert not only_expected, f"Missing keys: {only_expected}"
    assert not different, f"Different values for keys: {different}"

    assert collisions == {
        "foo": ["snippets_b.json"]
    }, f"Unexpected collisions: {collisions}"

    out_path = base / "combined_test_output.json"
    write_snippets(out_path, combined)
    print("Test passed. Combined output written to", out_path)


if __name__ == "__main__":
    run_test()
