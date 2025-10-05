from IPython import get_ipython

if "error_count" not in globals():
    error_count = 0


def _count_post_run_cell(result):
    global error_count
    if result.error_in_exec is not None:
        error_count += 1


ip = get_ipython()
if not hasattr(ip, "_error_hook_registered"):
    ip.events.register("post_run_cell", _count_post_run_cell)
    ip._error_hook_registered = True

error_count
