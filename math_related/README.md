# Math Related Module

Math, statistics, and numerical computing tutorials and utilities.

## Structure

- **np_related/** – NumPy fundamentals and idioms (broadcasting, ufuncs, random, sorting)
- **distributions/** – Probability distributions (normal, t, gamma, lognormal) and sampling demos
- **probability/** – Probability theory notes and visualizations
- **stats/** – Statistical measures (correlation, PSI), hypothesis testing
- **optimization/** – Optimization with SciPy and Mystic, constraint examples
- **simulation/** – Sampling simulations and experiments
- **matrix/** – Matrix operations and linear algebra snippets
- **formulas/** – Symbolic math and formula helpers
- **algorithms/** – General math algorithms
- **math_module/** – Standard library math usage
- **math_tute.py** – Grab-bag math notebook-style cheatsheet

## Reusable Utilities

### Math Utils (`math_utils.py`)

General-purpose helpers for teaching and quick experiments:

```python
from python_collection.math_related import math_utils

math_utils.set_random_seed(42)

# Softmax and sigmoid
probs = math_utils.softmax([1.0, 2.0, 3.0])
sig = math_utils.sigmoid([-1, 0, 1])

# Standardize and scale
z = math_utils.zscore([1, 2, 3, 4])
scaled = math_utils.normalize_minmax([10, 12, 15])

# Stable log-sum-exp
lse = math_utils.logsumexp([1000, 999, 998])

# Pairwise distances
import numpy as np
a = np.array([[0, 0], [1, 1]])
b = np.array([[1, 0], [2, 2]])
dists = math_utils.pairwise_distances(a, b)
```

## Running Examples

All scripts and notebooks are standalone.

```console
# Open NumPy notebooks
jupyter notebook math_related/np_related/

# Run distribution tutorial
python math_related/distributions/dist_tute.py

# Optimization with SciPy
python math_related/optimization/scipy_opt_tute.py

# Probability visuals
python math_related/probability/prob_tute.py
```

## Notes

- Dependencies: core examples use NumPy, pandas, matplotlib; some optimization demos use SciPy and Mystic.
- Keep scripts self-contained; avoid cross-imports unless using the utilities above.
- Set seeds for reproducibility in simulations (see `math_utils.set_random_seed`).
