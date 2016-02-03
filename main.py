from threading import Thread
from System import *
from Monitor import *


def system_handler(hsys):
    pass


def process_handler(hcpu, hproc):
    hcpu.run(hproc)


def memory_handler():
    pass


def disk_handler():
    pass


def network_handler():
    pass


monitor = Monitor()
s = System()
c = CPU(monitor)
m = Memory()
d = Disk()
n = Network(monitor)

s.processes = s.get_processes_dict()
s.create_process_handle_dict(s.processes)
# print s.processes

while True:
    hprocs = s.run()

    # for proc in hprocs:
    #     monitor_cpu_thread = Thread(target=process_handler, args=(c, proc))
    #     monitor_cpu_thread.start()


# monitor_cpu_thread = Thread(target=monitor.cpu_warning)
# network_thread = Thread(target=n.run)
# monitor_network_thread = Thread(target=monitor.Network_warning)
#
# monitor_cpu_thread.start()
# network_thread.start()
# monitor_network_thread.start()
