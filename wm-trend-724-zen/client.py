#!/usr/bin/env python3

import sys
import socket
from telnetlib import KERMIT

CHUNK_SIZE = 8
SEPARATOR = b'\x00'


def format_message(msg):
    """Format Message."""
    result = []
    if not msg:
        return ''
    for i in range(0, len(msg), 2):
        for char in msg[i:i+2]:
            result.append(f'{char:#04x}')

    return ' '.join(result)


def read_message(sock):
    """Read Message from socket."""
    buffer = bytes()
    while True:
        chunk = bytes(sock.recv(CHUNK_SIZE))
        # print(f'0x{chunk.hex()}')
        if not chunk:
            yield buffer
            break
        buffer += chunk
        while True:
            try:
                part, buffer = buffer.split(SEPARATOR, 1)
            except ValueError:
                break
            else:
                yield part


def main():
    """Do all the things."""
    if len(sys.argv) < 2:
        raise ValueError('missing required argument hostname')

    port = 8899
    if len(sys.argv) == 3:
        port = int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((sys.argv[1], port))
        messages = read_message(s)
        for message in messages:
            print(format_message(message))


try:
    main()
except KeyboardInterrupt:
    sys.exit(0)
