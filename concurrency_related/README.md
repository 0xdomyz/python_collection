# Concurrency Related

AsyncIO, threading, and multiprocessing demos. Scripts are standalone; utilities provided for reuse.

## Structure
- **asyncio_script/** – AsyncIO examples (`async_request.py`, db async demo)
- **multiprocessing_script/** – Multiprocessing examples
- **threading_script/** – Threading examples
- **concurrency_utils.py** – Small reusable helpers

## Utilities
```python
from python_collection.concurrency_related import concurrency_utils as cu

# Concurrency-limited gather
results = await cu.gather_with_concurrency(5, (fetch(url) for url in urls))

# Batch run callables returning coroutines
results = await cu.run_in_batches(10, [lambda u=u: fetch(u) for u in urls])

# Timeout with cancel
resp = await cu.cancel_on_timeout(fetch(url), timeout=2.0)
```

## Running Examples
```console
# Async HTTP crawl demo
python concurrency_related/asyncio_script/async_request.py

# Async DB demo
python concurrency_related/asyncio_script/db_related/long_running_task_db.py

# Threading demo
python concurrency_related/threading_script/tute.py

# Multiprocessing demo
python concurrency_related/multiprocessing_script/doco.py
```

## Notes
- Keep examples self-contained; no sys.path tweaks.
- For network/db demos, configure endpoints/credentials before running.
- Use `pip install -e .` to import utilities under `python_collection.concurrency_related`.
