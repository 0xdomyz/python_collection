import http.server
import socketserver
import threading
import time

# Define the directory to serve and the port
directory_to_serve = '/path/to/your/image/directory'
port = 8000

class TimeoutHTTPServer(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

# Change the working directory
os.chdir(directory_to_serve)

# Create the server
with socketserver.TCPServer(("", port), TimeoutHTTPServer) as httpd:
    print(f"Serving directory {directory_to_serve} at http://localhost:{port}")

    # Start the server in a new thread
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()

    # Wait for 10 seconds
    time.sleep(10)

    # Shut down the server
    httpd.shutdown()
    server_thread.join()