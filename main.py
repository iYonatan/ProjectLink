from threading import Thread
from Monitor import *
from System import *


def process_handler(hcpu, pid, name_handle_proc):
    process_dict = {pid: name_handle_proc}
    hcpu.run(process_dict)


def memory_handler(hmemo, pid, name_handle_proc):
    process_dict = {pid: name_handle_proc}
    hmemo.run(process_dict)


def disk_handler():
    pass


def network_handler():
    pass


monitor = Monitor()
s = System()
c = CPU(monitor)
m = Memory(monitor)
d = Disk()
n = Network(monitor)


d.run()

# network_thread = Thread(target=n.run)
# monitor_network_thread = Thread(target=monitor.Network_warning)
#
# network_thread.start()
# monitor_network_thread.start()
#
# s.processes = s.get_processes_dict()
# s.create_process_handle_dict(s.processes)
#
# for proc in s.processes:
#     monitor_cpu_thread = Thread(target=process_handler, args=(c, proc, s.processes[proc]))
#     monitor_cpu_thread.start()
#
#     monitor_memory_thread = Thread(target=memory_handler, args=(m, proc, s.processes[proc]))
#     monitor_memory_thread.start()
#
# while True:
#     opened_proc, closed_proc = s.run()
#     if len(opened_proc) > 0:
#         for proc in opened_proc:
#             monitor_cpu_thread = Thread(target=process_handler, args=(c, proc, opened_proc[proc]))
#             monitor_cpu_thread.start()
#
#             monitor_memory_thread = Thread(target=memory_handler, args=(m, proc, s.processes[proc]))
#             monitor_memory_thread.start()
#
#     if len(closed_proc) > 0:
#         pass
#
#     time.sleep(1)
