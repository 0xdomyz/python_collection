#!/usr/bin/env python3

import selectors
import socket
import sys
import types
from loguru import logger

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    logger.info(f"accepting...")
    conn, addr = sock.accept()  # Should be ready to read
    logger.info(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    mask = (
        selectors.EVENT_READ | selectors.EVENT_WRITE
    )  # want to know? when client con is ready for both
    sel.register(conn, mask, data=data)


def service_connection(key: selectors.SelectorKey, mask: int):
    sock, data = key.fileobj, key.data
    if mask & selectors.EVENT_READ:
        logger.info(f"receiving...")
        recv_data = sock.recv(1024)  # Should be ready to read
        logger.info(f"received data: {recv_data!r}")
        if recv_data:
            data.outb += recv_data
        else:  # check if no data received, which is client closing sock
            logger.info(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:  # always be the case for health sock
        if data.outb:
            logger.info(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]  # discard bytes sent


if len(sys.argv) != 3:
    logger.info(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

# create bind listen a tcp socket
host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
lsock.setblocking(False)  # calls to socket methods no longer block
logger.info(f"Listening on {(host, port)}")

sel.register(lsock, selectors.EVENT_READ, data=None)  # data stored w/ sock
# When you register a socket with selectors.EVENT_READ, the selector waits for the OS
# to signal that the socket is ready to read (for a listening socket,
# this means a new connection is waiting to be accepted;
# for a client socket, it means data is available to read).

# event loop
try:
    while True:
        events = sel.select(timeout=None)  # block until events are available
        logger.debug(f"events available: {events}")
        for (
            key,  # file's backing descriptor, selected event mask, and attached data.
            mask,  # event mask
        ) in events:
            if key.data is None:  # from the listening socket
                accept_wrapper(key.fileobj)
            else:  # from a client socket
                service_connection(key, mask)  # mask is events that are ready
except KeyboardInterrupt:
    logger.info("Caught keyboard interrupt, exiting")
finally:
    sel.close()
