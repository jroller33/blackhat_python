# this is a simple network scanner that uses ARP requests to identify all the devices on a network

# *** THIS SCRIPT REQUIRES 'SUDO' PERMISSIONS ON LINUX, OR ADMIN PERMISSIONS ON WINDOWS! ***

from scapy.all import ARP, Ether, srp

# range of IP addresses from '192.168.1.0' to '192.168.1.255' 
# target_ip = "192.168.1.1/24"
target_ip = "192.168.232.129/24"

# make the ARP packet
arp = ARP(pdst=target_ip)

# ethernet broadcast ('ff:ff:ff:ff:ff:ff' MAC address is for broadcasting over the network)
ethernet_broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")

# stack the layers of the packet
packet = ethernet_broadcast/arp

# srp() sends and receives packets at layer 2
# result = srp(packet, timeout=3, verbose=0)[0]
result = srp(packet, timeout=60)[0]  # result is list of pairs in format: (sent_packet, received_packet)

# list of the clients located on the network. It will be filled up in the loop
clients = []

# for each response, append ip and mac address to 'clients' list
for sent, received in result:
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})


print("Devices on the network: ")
print("IP" + " "*18+"MAC")

for client in clients:
    print("{:16}    {}".format(client['ip'], client['mac']))