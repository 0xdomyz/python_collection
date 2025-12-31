"""Benchmark byte-level log parsing in Python vs Cython."""

import random
import string
import time
from pathlib import Path

import logparse


def make_line() -> bytes:
    user = random.choice(["alice", "bob", "carol", "dave"])
    path = "/api/" + random.choice(["ping", "jobs", "docs", "status"])
    status = random.choice(["200", "500", "404"])
    latency = str(random.randint(1, 2000))
    return f"{user},{path},{status},{latency}\n".encode()


def make_data(n: int = 200_000) -> list[bytes]:
    return [make_line() for _ in range(n)]


def py_count_fields(line: bytes, sep: int = 44) -> int:
    return line.count(bytes([sep])) + 1 if line else 0


def py_split_first(line: bytes, sep: int = 44):
    idx = line.find(bytes([sep]))
    if idx == -1:
        return line, b""
    return line[:idx], line[idx + 1 :]


def bench(lines):
    t0 = time.perf_counter()
    py_total = sum(py_count_fields(ln) for ln in lines)
    py_time = time.perf_counter() - t0

    t1 = time.perf_counter()
    cy_total = sum(logparse.count_fields(ln) for ln in lines)
    cy_time = time.perf_counter() - t1

    # Use split_first to prevent dead-code elimination
    sample = lines[0]
    py_head, _ = py_split_first(sample)
    cy_head, _ = logparse.split_first(sample)

    print(f"Python count_fields: {py_time:.3f}s total={py_total}")
    print(
        f"Cython count_fields: {cy_time:.3f}s total={cy_total} speedup x{py_time / cy_time:.1f}"
    )
    print(f"Example head py={py_head!r} cy={cy_head!r}")


if __name__ == "__main__":
    if not Path("logparse.pyd").exists() and not Path("logparse.so").exists():
        print("Extension not built. Run: python setup.py build_ext --inplace")
    lines = make_data()
    bench(lines)
