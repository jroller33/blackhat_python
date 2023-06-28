# this is a basic, multi-threaded TCP server

import socket
import threading

IP = '0.0.0.0'
PORT = 9998

def main():
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))

    # server listens with a max of 5 back-log connections
    server.listen(5)
    print(f'[*] Listening on {IP}:{PORT}')

    # main loop for server, where it waits for incoming connection
    while True:

        # receive client socket in 'client' variable and remote connection details in 'address' variable
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')

        # new thread object, pass client socket and point to handle_client()
        client_handler = threading.Thread(target=handle_client, args=(client,))

        # start the thread to handle client connection, now main server loop can handle another connection.
        client_handler.start()


def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')

        # sends message back to client
        sock.send(b'ACK')

if __name__ == '__main__':
    main()