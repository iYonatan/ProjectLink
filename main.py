from threading import Thread
from Monitor import *
from System import *
from Communication import *

# region INCTANCES

comm = Communication()
monitor = Monitor(comm)

s = System()
c = CPU(monitor)
m = Memory(monitor)
d = Disk(monitor)
n = Network(monitor)


# endregion


def CPU_MEMORY_DISK():
    while True:
        util = c.cpu_utilization()

        comm.send(["system", "CPU_util", util])
        time.sleep(3)
        comm.send(["system", "Memo_Free_Ram", m.memory_ram()[1]])
        time.sleep(3)
        comm.send(["System", "Disk_list", d.disk_dict])
        time.sleep(3)


def system_handler():
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

        if len(opened_proc) > 0:
            for proc in opened_proc:
                monitor_cpu_thread = Thread(target=cpu_handler, args=(c, proc, opened_proc[proc]))
                monitor_cpu_thread.start()

                monitor_memory_thread = Thread(target=memory_handler, args=(m, proc, s.processes[proc]))
                monitor_memory_thread.start()

                time.sleep(1)

        time.sleep(5)


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
    disk_thread = Thread(target=d.run)
    disk_thread.start()


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

    CPU_MEMORY_DISK_Thread = Thread(target=CPU_MEMORY_DISK)
    CPU_MEMORY_DISK_Thread.start()

    disk_handler()
    network_handler()
    system_handler()


def FIRST_SETUP():
    USERNAME = "iyonatan"
    PASSWORD = "123456"

    comm.sec.server_public_key = Security.import_key(comm.sock.recv(1024))  # The public key from the server
    comm.sock.send(cPickle.dumps([comm.sec.aes_key, comm.sec.mode, comm.sec.iv])+"\r\n")

    comm.send([USERNAME, PASSWORD])

    if_user_exist = comm.recv()
    if if_user_exist != '200 OK':  # The user doesn't exist
        print "User does not exist"
        return

    print if_user_exist

    UUID = s.get_computer_UUID()
    comm.send(["Computer", "Computer-ID", UUID])

    if_computer_exist = comm.recv()
    if if_computer_exist == '200 OK':
        return

    OS_version = s.get_os_version()
    comm.send(["Computer", "OS_version", OS_version])

    CPU_model = c.get_cpu_model()
    comm.send(["System", "CPU_model", CPU_model])

    CPU_num = c.get_cpu_num()
    comm.send(["System", "CPU_num", CPU_num])

    Memo_Total_Ram = m.memory_ram()[0]
    comm.send(["System", "Memo_Total_Ram", Memo_Total_Ram])

    # -- The server is ready to get the rest of the data data from the client -- #
    return


if __name__ == "__main__":
    FIRST_SETUP()
    main()
