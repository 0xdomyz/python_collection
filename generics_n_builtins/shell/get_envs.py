# %%

from __future__ import annotations

import os
import sys


def build_environment_rows() -> list[tuple[str, str]]:
    return sorted(
        ((key, value) for key, value in os.environ.items()),
        key=lambda item: item[0].casefold(),
    )


# %%
rows = build_environment_rows()


# %%
from pathlib import Path

for name, value in rows:
    print(f"{name}: {value}")

# %%
paths = [i for i in rows if i[0] == "PATH"][0][1]

# %%
for path in paths.split(os.pathsep):
    print(Path(path).as_posix())
