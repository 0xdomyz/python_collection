import os
import signal
import subprocess
import time

# Define the directory to serve and the port
directory_to_serve = '/path/to/your/image/directory'
port = 8000

# Start the server in a new process
server = subprocess.Popen(['python3', '-m', 'http.server', str(port)], cwd=directory_to_serve)

# Wait for a while (e.g., 10 seconds)
time.sleep(10)

# Then shut down the server
os.kill(server.pid, signal.SIGINT)