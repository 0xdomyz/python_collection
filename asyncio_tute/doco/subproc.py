# shell cmd with asyncio
import asyncio


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    print(f"[{cmd!r} exited with {proc.returncode}]")
    if stdout:
        print(f"[stdout]\n{stdout.decode()}")
    if stderr:
        print(f"[stderr]\n{stderr.decode()}")


asyncio.run(run("ls /zzz"))
asyncio.run(run("ls -la"))


# parallel
async def main():
    await asyncio.gather(run("ls /zzz"), run('sleep 1; echo "hello"'))


asyncio.run(main())

# process class to control a subprocess
import asyncio
import sys


async def get_date():
    code = "import datetime; print(datetime.datetime.now())"

    # Create the subprocess; redirect the standard output
    # into a pipe.
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-c", code, stdout=asyncio.subprocess.PIPE
    )

    # Read one line of output.
    data = await proc.stdout.readline()
    line = data.decode("ascii").rstrip()

    # Wait for the subprocess exit.
    await proc.wait()
    return line


date = asyncio.run(get_date())
print(f"Current date: {date}")
