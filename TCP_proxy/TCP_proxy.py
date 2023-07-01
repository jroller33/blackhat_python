import sys
import socket
import threading

# this proxy has 4 parts:
# - display communication between local and remote machines to the console (hexdump)
# - receive data from an incoming socket from either the local or remote machine (receive_from)
# - manage traffic direction between remote and local machines (proxy_handler)
# - set up a listening socket and pass it to proxy_handler (server_loop)


# HEXFILTER string contains ASCII characters, or a dot (.) if one doesn't exist
HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)]
)


# This function lets you watch the data going through the proxy in real time
def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):  # make sure it's a string, decode the bytes if it's a byte string
        src = src.decode()

    results = list()
    for i in range(0, len(src), length):

        word = str(src[i:i+length]) # take a piece of the string and put it in 'word'

        # use 'translate()' to substitute the str representation of each char for the corresponding char in the raw string (printable)
        printable = word.translate(HEX_FILTER)  

        # substitute the hex representation of the int value of every char in the raw string (hexa)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length * 3

        # 'results' is a new list to hold the strings, contains the hex value of the index of teh first byte in the word, the hex value of the word, and its printable representation.
        results.append(f'{i:04x}  {hexa:<{hexwidth}}  {printable}')

    if show:
        for line in results:
            print(line)
    else:
        return results
    

def receive_from(connection): # for receiving local and remote data, pass in the socket object (connection) it will use
    buffer = b""              # create an empty byte string that accumulates responses from the socket

    connection.settimeout(10)      # 10 second timeout. For proxying traffic to other countries or over subpar networks, set the timeout longer
    try:
        while True:
            data = connection.recv(4096)    # reads response data into the buffer, until there's no more data or it reaches timeout
            if not data:
                break
            buffer += data

    except Exception as e:
        pass
    return buffer   # return 'buffer' byte string to the caller (could be local or remote machine)

def request_handler(buffer):
# TODO: modify request packets before proxy sends them
    return buffer

def response_handler(buffer):
# TODO: modify response packets before proxy sends them
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[<==] Sending %d bytes to localhost." & len(remote_buffer))
        client_socket.send(remote_buffer)