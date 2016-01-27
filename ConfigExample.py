from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('Config.ini')

SLEEP_TIME_1_5 = parser.get('Pywin32', 'KERNEL_32')
print SLEEP_TIME_1_5
