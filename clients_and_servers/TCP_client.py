# this is a simple TCP client using the `socket` module

# this script is made with three assumptions:
# 1. our connection will always succeed
# 2. server expects us to send data first
# 3. server will always return data quickly

import socket

target_host = "0.0.0.0"
target_port = 9998


# create a socket object and connect the client
# .AF_INET means we're using IPv4, .SOCK_STREAM means it's TCP not UDP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))


# send data as bytes to the server
client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

# receive data
response = client.recv(4096)

print(response.decode())
client.close()
