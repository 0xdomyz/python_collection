# %%
import os
from pathlib import Path

path = Path(".")


# %%
def reformat(func_str: str) -> str:
    res = []
    for line in func_str.strip().splitlines():
        line = line.replace('"', '\\"')
        n_spaces_at_start = len(line) - len(line.lstrip())
        res.append(f'"{" " * n_spaces_at_start}{line.strip()}",')

    return "\n".join(res)


# %%
func_str = """
xxx
"""

print(reformat(func_str))
