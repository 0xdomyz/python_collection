# %%
import itertools
import math

import pandas as pd

# %% [markdown]
# ## possibilities
# ####################################################################################################
# %%
factor_levels = {
    # fmt: off
    "A": ["P1", "P2", "P3", "Missing"],
    "B": ["r1", "r2"],
    "C": ["in", "out"],
    "D": ["US", "EU", "APAC"],
    # fmt: on
}
factor_levels
# %%
key_factor_levels = {
    # fmt: off
    "A": ["P1", "P2"],
    "B": ["r1", ],
    "C": ["in", "out"],
    "D": [],
    # fmt: on
}
key_factor_levels
# %%
factor_levels_wo_factor_a = {k: v for k, v in factor_levels.items() if k != "A"}
factor_levels_wo_factor_a
# %%
levels = [len(l) for l in factor_levels.values()]
levels
# %%
levels_plus_1 = [i + 1 for i in levels]
levels_plus_1
# %%
n = 3
n_combos_example = [math.comb(n, r) for r in range(2, n)]
n_combos_example
# %%
pure_multi_levels = [math.prod(math.comb(n, r) for r in range(2, n)) for n in levels]
pure_multi_levels = [0 if i == 1 else i for i in pure_multi_levels]
pure_multi_levels
# %%
multi_levels = [a + b for a, b in zip(levels_plus_1, pure_multi_levels)]
multi_levels

# %%
n_all_choose_all = 1
n_test_1_factor_only = sum(levels)
n_test_1_factor_only_wo_a = sum(len(l) for k, l in factor_levels_wo_factor_a.items())
n_single_choice_all_combos = math.prod(levels_plus_1)
n_single_choice_all_combos_wo_a = math.prod(
    i + 1 for i in [len(l) for k, l in factor_levels_wo_factor_a.items()]
)
n_single_choice_all_combos_key = math.prod(
    i + 1 for i in [len(l) for k, l in key_factor_levels.items()]
)
n_multi_choice_all_combos = math.prod(multi_levels)

print(f"{n_all_choose_all = }")
print(f"{n_test_1_factor_only = }")
print(f"{n_test_1_factor_only_wo_a = }")
print(f"{n_single_choice_all_combos = }")
print(f"{n_single_choice_all_combos_wo_a = }")
print(f"{n_single_choice_all_combos_key = }")
print(f"{n_multi_choice_all_combos = }")
