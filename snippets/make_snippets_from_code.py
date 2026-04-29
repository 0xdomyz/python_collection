# %%
from pathlib import Path


def reformat(func_str: str) -> str:
    res = []
    for line in func_str.strip().splitlines():
        line = line.replace('"', '\\"')
        n_spaces_at_start = len(line) - len(line.lstrip())
        res.append(f'"{" " * n_spaces_at_start}{line.strip()}",')

    return "\n".join(res)


# %%
# 1 str
func_str = """

"""

print(reformat(func_str))

# %%
# file content
with open(
    r"C:\Users\yzdom\Projects\python_collection\snippets\test_snippets_saspy.py", "r"
) as f:
    func_str = f.read()
res = reformat(func_str)

with open("res.txt", "w") as f:
    f.write(res)
