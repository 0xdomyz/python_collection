import subprocess


def measure_temp():
    completed_proc = subprocess.run(
        "vcgencmd measure_temp", shell=True, capture_output=True
    )
    completed_proc.check_returncode()
    return completed_proc.stdout.decode("utf-8")
