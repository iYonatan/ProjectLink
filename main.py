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

for proc in s.processes:
    monitor_cpu_thread = Thread(target=process_handler, args=(c, s.processes[proc]))
    monitor_cpu_thread.start()

while True:
    opened_proc, closed_proc = s.run()
    if len(opened_proc) > 0:
        for proc in opened_proc:
            monitor_cpu_thread = Thread(target=process_handler, args=(c, opened_proc[proc]))
            monitor_cpu_thread.start()

# monitor_cpu_thread = Thread(target=monitor.cpu_warning)
# network_thread = Thread(target=n.run)
# monitor_network_thread = Thread(target=monitor.Network_warning)
#
# monitor_cpu_thread.start()
# network_thread.start()
# monitor_network_thread.start()
