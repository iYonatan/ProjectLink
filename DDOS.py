"""
 Works only on Python 2.6
"""

from scapy.all import *
from scapy.layers.inet import IP, TCP


send(IP(dst='localhost') / TCP(flags='S', sport=RandShort(), dport=80), varbose=True, loop=True)

