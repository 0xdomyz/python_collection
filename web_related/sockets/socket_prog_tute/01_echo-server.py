#!/usr/bin/env python3

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()  # make listening socket
    conn, addr = s.accept()  # block and wait
    with conn:  # use the new socket
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)  # blocking
            if not data:  # signal of client disconnect
                break
            conn.sendall(data)
    # go out of with, socket is closed
