from ConfigParser import SafeConfigParser
from ctypes import *
from pywin32_Structs import *

parser = SafeConfigParser()
parser.read('Config.ini')

ICMP = int(parser.get('Socket', 'ICMP'))

parser.set('Socket', 'ICMP', str(16))
ICMP = int(parser.get('Socket', 'ICMP'))
print ICMP
