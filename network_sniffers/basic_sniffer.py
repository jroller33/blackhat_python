# sniffer's main purpose is to discover hosts on a target network
# it needs to work on Windows and Linux, even though the process of accessing raw sockets is different on Windows and Linux

# in this basic example, there's a raw socket sniffer that reads a single packet and then quits

import socket
import os

# host to listen on 
HOST = '192.168.1.203'


# this is using promiscuous mode, which requires admin privileges on Windows or root on Linux
# promiscuous mode lets you sniff all packets on the network card, even if it's not destined for your host
def main():
    if os.name == 'nt':                         
        socket_protocol = socket.IPPROTO_IP     # Windows lets you sniff all incoming packets, regardless of protocol
    else:                                       
        socket_protocol = socket.IPPROTO_ICMP   # Linux makes you specify you're sniffing ICMP packets

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))

    # socket option that includes the IP headers from captured packets
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # check if it's Windows. If so, send IOCTL to network card driver to enable promiscuous mode
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    # prints out one raw packet, without any decoding
    print(sniffer.recvfrom(65565))

    # if Windows, now disable promiscuous mode
    if os.name == 'nt': 
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

if __name__ == '__main__':
    main()