import multiprocessing as mp
import queue
import time
import traceback


def _worker(target, args, kwargs, result_queue):
    try:
        target(*args, **kwargs)
        result_queue.put(("ok", ""))
    except Exception:
        result_queue.put(("error", traceback.format_exc()))


def _run_once(target, args, kwargs, timeout):
    ctx = mp.get_context("spawn")
    result_queue = ctx.Queue()
    process = ctx.Process(
        target=_worker,
        args=(target, args, kwargs, result_queue),
        daemon=True,
    )
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join(5)
        if process.is_alive():
            process.kill()
            process.join(2)
        return False, f"Child process timed out after {timeout} seconds"

    status = None
    details = ""
    try:
        status, details = result_queue.get_nowait()
    except queue.Empty:
        status = None

    if process.exitcode == 0 and status == "ok":
        return True, ""

    if status == "error":
        return False, details

    return False, f"Child process exited unexpectedly with code {process.exitcode}"


def run_in_isolated_process(target, *args, timeout=90, attempts=3, **kwargs):
    failures = []
    for attempt in range(1, attempts + 1):
        ok, message = _run_once(target, args, kwargs, timeout)
        if ok:
            return True, ""
        failures.append(f"Attempt {attempt}/{attempts} failed: {message}")
        time.sleep(0.5 * attempt)

    return False, "\n\n".join(failures)
