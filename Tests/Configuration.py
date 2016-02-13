from ConfigParser import SafeConfigParser


parser = SafeConfigParser()
parser.read('Config.ini')

SLEEP_TIME_1_5 = float(parser.get('DEFAULT', 'SLEEP_TIME_1_5'))
PERCENT_LIMIT = int(parser.get('DEFAULT', 'PERCENT_LIMIT'))
ENT_LINE = parser.get('DEFAULT', 'ENT_LINE')
UNLIMITED_LOOP = int(parser.get('DEFAULT', 'UNLIMITED_LOOP'))

NORMAL_CPU_USAGE = int(parser.get('System', 'NORMAL_CPU_USAGE'))
NORAML_PROCESS_USAGE = int(parser.get('System', 'NORAML_PROCESS_USAGE'))
PROCESS_TIMES_TIME = float(parser.get('System', 'PROCESS_TIMES_TIME'))
PROCESS_NAME = int(parser.get('System', 'PROCESS_NAME'))
PROCESS_HANDLE = int(parser.get('System', 'PROCESS_HANDLE'))

HOST_IP = parser.get('Socket', 'HOST_IP')
PORT = int(parser.get('Socket', 'PORT'))
MAX_PACKET_RECIVER = int(parser.get('Socket', 'MAX_PACKET_RECIVER'))
ICMP = int(parser.get('Socket', 'ICMP'))
TCP = int(parser.get('Socket', 'TCP'))
UDP = int(parser.get('Socket', 'UDP'))