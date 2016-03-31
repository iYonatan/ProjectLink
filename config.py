from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('Config.ini')


class default(object):
    ZERO = int(parser.get('DEFAULT', 'ZERO'))
    ONE = int(parser.get('DEFAULT', 'ONE'))
    WAIT_1_SEC = int(parser.get('DEFAULT', 'WAIT_1_SEC'))
    WAIT_3_SEC = int(parser.get('DEFAULT', 'WAIT_3_SEC'))
    WAIT_1_5_SEC = float(parser.get('DEFAULT', 'WAIT_1_5_SEC'))
    PERCENT_LIMIT = int(parser.get('DEFAULT', 'PERCENT_LIMIT'))
    ENT_LINE = parser.get('DEFAULT', 'ENT_LINE')
    UNLIMITED_LOOP = int(parser.get('DEFAULT', 'UNLIMITED_LOOP'))


class system(object):
    NORMAL_CPU_USAGE = int(parser.get('System', 'NORMAL_CPU_USAGE'))
    NORAML_PROCESS_USAGE = int(parser.get('System', 'NORAML_PROCESS_USAGE'))
    PROCESS_TIMES_TIME = float(parser.get('System', 'PROCESS_TIMES_TIME'))
    PROCESS_NAME = int(parser.get('System', 'PROCESS_NAME'))
    PROCESS_HANDLE = int(parser.get('System', 'PROCESS_HANDLE'))


class network(object):
    PORT = int(parser.get('Socket', 'PORT'))
    MAX_PACKET_RECIVER = int(parser.get('Socket', 'MAX_PACKET_RECIVER'))
    ICMP = int(parser.get('Socket', 'ICMP'))
    TCP = int(parser.get('Socket', 'TCP'))
    UDP = int(parser.get('Socket', 'UDP'))


class response(object):
    OK_200 = parser.get('Response', '200_OK')
    NOT_FOUND_400 = parser.get('Response', '400_NOT_FOUND')


class user(object):
    USERNAME = None
    HASH_PASSWORD = None

