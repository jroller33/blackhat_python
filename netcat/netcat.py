import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading


# receives a cmd, runs it, and returns the output as a string
def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    
    # 'check_output' method runs a cmd on the local OS and returns the output from the cmd
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()


class NetCat:
    # init NetCat object with arguments from command line and buffer
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # create the socket object
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def run(self):  # run() has two functions: listen() and send()
        if self.args.listen:
            self.listen()
        else:
            self.send()


    def send(self):
        self.socket.connect((self.args.target, self.args.port))  # connect to the target and port
        if self.buffer:                                          # if there's a buffer, send it to the target first
            self.socket.send(self.buffer)

        # try/except block is so you can exit the connection with 'CTRL-C'
        try:
            while True:     # receives data from the target
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break       # if there's no data, break the loop

                # print the response data and wait for input, then send the input and continue the loop
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())

        # loop continues until keyboard interrupt ('CTRL-C'), which closes the socket
        except KeyboardInterrupt:
            print('User terminated')
            self.socket.close()
            sys.exit()


    def listen(self):
        self.socket.bind((self.args.target, self.args.port))    # bind to target and port
        self.socket.listen(5)                                   # listens in a loop

        while True:
            client_socket, _ = self.socket.accept()

            # passes the connected socket to the 'handle' method
            client_thread = threading.Thread(
                target=self.handle, args=(client_socket,)
            )
            client_thread.start()


    # handle() executes whatever argument you pass in the command line: execute a command, upload a file, or start a shell
    def handle(self, client_socket):

        # if command needs to be executed, handle() passes the command to execute() and sends the output back on the socket
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())

        # if a file needs to be uploaded, set up a loop to listen on socket and receive data until there's no more data input
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:            
                    file_buffer += data

                else:
                    break

            # write data to the file
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)

            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())

        # if a shell needs to be created, set up a loop, send a prompt, and wait for a command string
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'JNC: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)

                    # execute() the command
                    response = execute(cmd_buffer.decode())

                    # return output of the command to the sender
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''

                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()



# 'argparse' module from python standard library to create a CLI
# pass arguments to it so it can upload a file, execute a command or start a shell

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="John's Netcat",
        formatter_class=argparse.RawDescriptionHelpFormatter,

        # this is the help menu
        epilog=textwrap.dedent('''Example:
        netcat.py -t 192.168.1.108 -p 5555 -l -c     # command shell
        netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt     # upload to file
        netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\"    # execute command
        echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135    # echo text to server port 135
        netcat.py -t 192.168.1.108 -p 5555          # connect to server
    '''))

    # specifies how the netcat behaves
    parser.add_argument('-c', '--command', action='store_true', help='command shell')   # sets up a shell
    parser.add_argument('-e', '--execute', help='execute specified command')    # executes one command
    parser.add_argument('-l', '--listen', action='store_true', help='listen')   # sets up a listener
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')  
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')


    args = parser.parse_args()
    # if you set it up as a listener, NetCat object has an empty buffer string
    if args.listen:
        buffer = ''
    # else, send buffer content from 'stdin'
    else:
        buffer = sys.stdin.read()

    # starts up the NetCat with 'run' method
    nc = NetCat(args, buffer.encode())
    nc.run()
