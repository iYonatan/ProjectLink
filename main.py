from threading import Thread
from Monitor import *
from System import *

monitor = Monitor()
s = System()
c = CPU(monitor)
m = Memory(monitor)
d = Disk()
n = Network(monitor)


def cpu_handler(hcpu, pid, name_handle_proc):
    """
    Handles a process for the CPU
    :param hcpu: CPU() instance
    :param pid: A process id (int)
    :param name_handle_proc: (The name of the process (string) and the handle of the process) (tuple)
    :return:
    """
    process_dict = {pid: name_handle_proc}
    hcpu.run(process_dict)
    return


def memory_handler(hmemo, pid, name_handle_proc):
    """
    Handles a process for memory
    :param hmemo: Memory() instance
    :param pid: A process id (int)
    :param name_handle_proc: (The name of the process (string) and the handle of the process) (tuple)
    :return:
    """
    process_dict = {pid: name_handle_proc}
    hmemo.run(process_dict)
    return


def disk_handler():
    pass


def network_handler():
    """
    Handles the Network
    :return:
    """
    network_thread = Thread(target=n.run)
    monitor_network_thread = Thread(target=monitor.Network_warning)

    network_thread.start()
    monitor_network_thread.start()


def main():
    """
    This function runs everything
    :return:
    """
    network_handler()

    s.processes = s.get_processes_dict()
    s.create_process_handle_dict(s.processes)

    for proc in s.processes:
        monitor_cpu_thread = Thread(target=cpu_handler, args=(c, proc, s.processes[proc]))
        monitor_cpu_thread.start()

        monitor_memory_thread = Thread(target=memory_handler, args=(m, proc, s.processes[proc]))
        monitor_memory_thread.start()

        time.sleep(1)

    while True:
        opened_proc, closed_proc = s.run()

        time.sleep(5)

        if len(opened_proc) > 0:
            for proc in opened_proc:
                monitor_cpu_thread = Thread(target=cpu_handler, args=(c, proc, opened_proc[proc]))
                monitor_cpu_thread.start()

                monitor_memory_thread = Thread(target=memory_handler, args=(m, proc, s.processes[proc]))
                monitor_memory_thread.start()

                time.sleep(1)

        if len(closed_proc) > 0:
            continue




if __name__ == "__main__":
    main()
