import socket
import click


@click.command(
    help="""
Connects to the server and sends a message, then prints the echoed response.

Example usage:
    python 03_simple_echo_client.py --host 127.0.0.1 --port 65432 "Hello, world"
"""
)
@click.option("--host", default="127.0.0.1", help="Server hostname or IP address")
@click.option("--port", default=65432, type=int, help="Server port")
@click.argument("msg")
def echo_client(host, port, msg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(msg.encode())
        data = s.recv(1024)
    print(f"Received {data!r}")


if __name__ == "__main__":
    echo_client()
