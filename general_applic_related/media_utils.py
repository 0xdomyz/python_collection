"""
Small media utility helpers using only the standard library.
"""

import math
from pathlib import Path
from typing import Iterable, Tuple


def seconds_to_hms(seconds: float) -> str:
    """Convert seconds to HH:MM:SS.mmm string."""
    if seconds < 0:
        raise ValueError("seconds must be non-negative")
    msec = int(round((seconds - math.floor(seconds)) * 1000))
    total_secs = int(math.floor(seconds))
    h, rem = divmod(total_secs, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}.{msec:03d}"


def change_extension(path: str | Path, new_ext: str) -> Path:
    """Return a Path with a new extension (e.g., .mp3 -> .wav)."""
    p = Path(path)
    if not new_ext.startswith("."):
        new_ext = f".{new_ext}"
    return p.with_suffix(new_ext)


def ensure_unique_path(path: str | Path) -> Path:
    """Generate a non-clashing path by appending a counter if needed."""
    p = Path(path)
    if not p.exists():
        return p
    stem, suffix = p.stem, p.suffix
    parent = p.parent
    idx = 1
    while True:
        candidate = parent / f"{stem}_{idx}{suffix}"
        if not candidate.exists():
            return candidate
        idx += 1


def human_size(num_bytes: int) -> str:
    """Format bytes as a human-readable string."""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024.0 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"


def batch_paths(paths: Iterable[str | Path], batch_size: int) -> list[list[Path]]:
    """Group paths into batches of size `batch_size`."""
    batch: list[Path] = []
    result: list[list[Path]] = []
    for p in paths:
        batch.append(Path(p))
        if len(batch) == batch_size:
            result.append(batch)
            batch = []
    if batch:
        result.append(batch)
    return result
