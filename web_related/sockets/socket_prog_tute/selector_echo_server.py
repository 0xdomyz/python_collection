import selectors
import socket

sel = selectors.DefaultSelector()


def accept(sock, mask):
    # Accept a new client connection
    conn, addr = sock.accept()  # Should be ready
    print("accepted", conn, "from", addr)
    conn.setblocking(False)
    # Register the new connection for read events
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn, mask):
    # Read data from client
    data = conn.recv(1000)  # Should be ready
    if data:
        print("echoing", repr(data), "to", conn)
        # Echo the received data back to client
        conn.send(data)  # Hope it won't block
    else:
        print("closing", conn)
        # Unregister and close connection if no data
        sel.unregister(conn)
        conn.close()


# Create listening socket
sock = socket.socket()
sock.bind(("localhost", 1234))
sock.listen(100)
sock.setblocking(False)
# Register listening socket for accept events
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    # Wait for events
    events = sel.select()
    for key, mask in events:
        # Call the registered callback (accept or read)
        callback = key.data
        callback(key.fileobj, mask)
