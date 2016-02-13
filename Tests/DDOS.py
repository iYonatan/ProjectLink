"""
 Works only on Python 2.6
"""

from scapy.all import *

send(IP(dst='localhost') / TCP(flags='S', sport=RandShort(), dport=80), verbose=True, loop=True)

