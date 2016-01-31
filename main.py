from threading import Thread
from System import *
from Monitor import *
from multiprocessing.pool import ThreadPool

monitor = Monitor()
s = System()
c = CPU()
m = Memory()
d = Disk()
n = Network(monitor)

pool = ThreadPool(processes=1)

hprocs = s.get_processes_list()

t = time.time()
for proc in hprocs:
    print proc
    c.cpu_utilization()
    async_result = pool.apply_async(c.cpu_process_util, (proc, ))
    # process_cpu_thread = Thread(target=c.cpu_process_util, args=(proc, ))
    # process_memo_thread = Thread(target=m.memory_process_usage, args=(proc, ))
    return_val = async_result.get()
    print return_val
    # process_cpu_thread.start()
    # process_memo_thread.start()

print round(time.time() - t)

# monitor_cpu_thread = Thread(target=monitor.cpu_warning)
# network_thread = Thread(target=n.run)
# monitor_network_thread = Thread(target=monitor.Network_warning)
#
# monitor_cpu_thread.start()
# network_thread.start()
# monitor_network_thread.start()
