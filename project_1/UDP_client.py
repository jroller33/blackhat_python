import socket

target_host = "127.0.0.1"
target_port = 9997

# create a socket object
# .AF_INET means IPv4, .SOCK_DGRAM means UDP not TCP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send data
client.sendto(b"AAABBBCCC", (target_host, target_port))

# receive data
data, addr = client.recvfrom(4096)

print(data.decode)
client.close()
