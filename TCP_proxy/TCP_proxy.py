# this proxy has 4 parts:
# hexdump() - displays the data traveling between local and remote machines to the console
# receive_from() - receives data from an incoming socket from either the local or remote machine
# proxy_handler() - manages traffic direction between remote and local machines
# server_loop() - sets up a listening socket and passes it to proxy_handler()


import sys
import socket
import threading

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
    remote_socket.connect((remote_host, remote_port))       # connect to remote host

    # check if it needs to first start a connection to the remote side and request data before going into main loop. Example: FTP servers send a banner first
    if receive_first:
        remote_buffer = receive_from(remote_socket)     # receive_from() accepts a connected socket object and receives data
        hexdump(remote_buffer)                          # dump the contents of the packet so you can inspect it

    remote_buffer = response_handler(remote_buffer)     # give output to response_handler()
    if len(remote_buffer):
        print("[<==] Sending %d bytes to localhost." & len(remote_buffer))
        client_socket.send(remote_buffer)               # send the received buffer to local client


    # this loop continuously reads from the local client, processes the data, and sends it to the remote client,
    # reads from the remote client, processes data, sends it to the local client, until it no longer detects any data
    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = "[==>]Received %d bytes from localhost." % len(local_buffer)
            print(line)
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost.")

        # if there's no data to send on either side of the connection, close both the local and remote sockets and break the loop.
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break


# sets up and manages the connection
def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # create a socket
    try:
        server.bind((local_host, local_port))       # bind the socket to the local host and listen

    except Exception as e:                   # show error if it couldn't bind to the local_host and listen on local_port
        print('problem trying to bind: %r' % e)
        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check permissions or other listening sockets")
        sys.exit(0)

    print("[*] Listening on %s:%d" % (local_host, local_port))
    server.listen(5)


    while True:
        client_socket, addr = server.accept()   # new connection request comes in

        # prints out the local connection info
        line = "> Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)

        # starts a thread to talk to remote_host
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first)
        )
        proxy_thread.start()


# input command line arguments
def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./TCP_proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first (Boolean)]")
        print("Example: ./TCP_proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False
    
    # start server loop that listens for connections
    server_loop(local_host, local_port, remote_host, remote_port, receive_first) 

if __name__ == '__main__':
    main()