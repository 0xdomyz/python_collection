# GitHub Copilot Instructions

## Project Overview
This is a **learning-focused Python collection** containing tutorial scripts, notebooks, and examples across data science, ML, web development, concurrency, and systems programming domains. Files are executable demonstrations and references, not production code.

## Project Structure

### Organization by Domain
- `model_related/` - ML/stats models (sklearn, statsmodels, PyMC3, torch, keras, tensorflow)
- `data_related/` - Data manipulation (pandas, APIs, databases, cleaning)
- `plot_related/` - Visualization (matplotlib, seaborn, plotly, streamlit apps)
- `math_related/` - Math utilities (numpy, scipy, sympy, distributions, optimization)
- `web_related/` - Web tools (requests, websockets, scraping, servers, email)
- `concurrency_related/` - Async/threading/multiprocessing examples
- `dashboards/` - Dash and Streamlit interactive applications
- `generics_n_builtins/` - Core Python (classes, imports, logging, config, regex, testing)
- `c_related/cython_scripts/` - Cython compilation examples
- `computer science related/` - CS fundamentals notes

### Key Files
- `snippets/*.json` - VS Code snippets for common patterns (imports, pandas operations, db queries)
- `learning_with_llm.md` - Structured learning methodology for LLM-assisted study

## Coding Conventions

### Script Structure
Most scripts are **standalone, self-documenting demonstrations**:
- No main guards unless showing async patterns (`if __name__ == "__main__": asyncio.run(main())`)
- Direct execution with `plt.show()` for visualization scripts
- Streamlit apps run with `python -m streamlit run <file.py>`

### Import Patterns
Standard library order, then third-party (numpy/pandas/matplotlib first):
```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_iris
```

### Code Organization
- **Prefer self-contained scripts**: Each example should be runnable independently without cross-imports
- **For shared utilities**: Create a proper package structure with `pyproject.toml` or `setup.py`, then install in editable mode:
  ```console
  pip install -e .
  ```
- **Avoid `sys.path` manipulation**: Don't add paths to `sys.path` - this breaks portability and proper Python packaging conventions
- **For notebooks**: Either keep self-contained or install the project as a package first

### Pandas Conventions
- Method chaining with `.assign()` for transformations (see `model_related/dataset.py`)
- Lambda functions inline: `df.assign(new_col=lambda x: x.old_col * 2)`
- Prefer `.loc` and `.select_dtypes()` for column selection

### Cython Workflow
For Cython scripts in `c_related/cython_scripts/`:
```console
python setup.py build_ext --inplace
```
Or in Jupyter: `%load_ext Cython` then `%%cython --annotate`

## Development Workflows

### Running Examples
- **Python scripts**: Direct execution via `python <file>.py` (most have no args)
- **Jupyter notebooks**: Open in VS Code or Jupyter (238+ notebooks in project)
- **Streamlit apps**: `python -m streamlit run <file>.py`
- **Async scripts**: Use `asyncio.run()` pattern (see `concurrency_related/asyncio_script/async_request.py`)

### Testing
Minimal pytest setup in `generics_n_builtins/tests/`. Run with `pytest` from project root.

### Common Tasks
- Use snippets via prefix triggers: `peq` (print with f-string), `syspath` (add to sys.path), `dbsetup` (sqlite connection)
- Logging setup follows `generics_n_builtins/log/logging_tute.py` or `generics_n_builtins/log/loguru_tute.py`
- argparse patterns in `generics_n_builtins/layout/argparse_related/`

## AI Agent Guidance

### When Creating New Files
- Place in appropriate domain folder (create subdirectory if needed for multi-file topics)
- Use descriptive names: `<topic>_tute.py` or `<concept>_example.py`
- Include docstring at top for complex examples explaining usage/context
- Add to snippets if pattern is reusable (format matches `snippets/snippets_general.json`)

### When Reading Existing Code
- Files are self-contained demonstrations, not interdependent modules (except explicit import examples)
- Empty `__init__.py` files mark package boundaries but modules don't cross-import
- Look in `snippets/` for reusable patterns before creating new utilities
- Check `learning_with_llm.md` for learning methodology context

### Domain-Specific Notes
- **Data scripts**: Data files in `data_related/toydata/` or external URLs (see `plot_related/mpl_notes/contents/get_data/get_data.py`)
- **Model scripts**: Often use sklearn toy datasets (`load_iris`, `make_blobs`)
- **Web scripts**: May include hardcoded URLs for examples (e.g., S3 demo data in streamlit examples)
- **Plot scripts**: Call `plt.show()` at end; notebook versions omit this
