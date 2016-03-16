from threading import Thread
from Monitor import *
from System import *
from Communication import *
from config import *
from GUI import GUI

# region INCTANCES

# Handles the communication and the security with the server
comm = Communication()
# Handles the project decisions and warns if necessary
monitor = Monitor(comm)

s = System()  # Instance of System class
c = CPU(monitor)  # Instance of CPU class
m = Memory(monitor)  # Instance of Memory class
d = Disk(monitor)  # Instance of Disk class
n = Network(monitor)  # Instance of Network class

# First decleration of the GUI class
gui = GUI()


# endregion

def user_handle(gui):
    """
    Callback function. The function is invoked when a user clicked on the submit button ("Login") afrer entring two
    inputs: Username and Password. The fucntion takes these inputs and send them to the server. The server returns if
    the username and the password exist in the database. If the do, the GUI will close itself and the code will continue
    otherwise, the GUI will keep asking for username and password until the server accepts them.

    :param gui:
    :return: None
    """

    # Get the inputs from the GUI: Username and password input
    USERNAME = gui.username_input.get()
    PASSWORD = gui.pwd_input.get()

    print USERNAME, PASSWORD
    # Sends Username and password that the user inputed
    comm.send([USERNAME, PASSWORD])

    # Recives user status from the server
    if_user_exist = comm.recv()

    # If the user exists, the GUI will kill itself in order to continue the rest of the code, otherwise the GUI will
    # keep running until the user inputed currect username and password
    if if_user_exist == response.OK_200:
        gui.success_login()
        gui.destroy()
        return

    gui.failed_login()


def CPU_MEMORY_DISK():
    while default.UNLIMITED_LOOP:
        util = c.cpu_utilization()
        comm.send(["system", "CPU_util", util])
        time.sleep(default.WAIT_3_SEC)
        comm.send(["system", "Memo_Free_Ram", m.memory_ram()[1]])
        time.sleep(default.WAIT_3_SEC)


def system_handler():
    s.processes = s.get_processes_dict()
    s.create_process_handle_dict(s.processes)

    for proc in s.processes:
        monitor_cpu_thread = Thread(target=cpu_handler, args=(c, proc, s.processes[proc]))
        monitor_cpu_thread.start()

        monitor_memory_thread = Thread(target=memory_handler, args=(m, proc, s.processes[proc]))
        monitor_memory_thread.start()

        time.sleep(default.WAIT_1_SEC)

    while default.UNLIMITED_LOOP:
        opened_proc, closed_proc = s.run()

        if len(opened_proc) > default.ZERO:
            for proc in opened_proc:
                monitor_cpu_thread = Thread(target=cpu_handler, args=(c, proc, opened_proc[proc]))
                monitor_cpu_thread.start()

                monitor_memory_thread = Thread(target=memory_handler, args=(m, proc, s.processes[proc]))
                monitor_memory_thread.start()

                time.sleep(default.WAIT_1_SEC)

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
    disk_monitor_thread = Thread(target=d.run)
    disk_monitor_thread.start()

    while default.UNLIMITED_LOOP:
        comm.send(["system", "Disk_list", d.disk_dict])
        time.sleep(1800)


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

    disk_thread = Thread(target=disk_handler)
    disk_thread.start()

    CPU_MEMORY_DISK_Thread = Thread(target=CPU_MEMORY_DISK)
    CPU_MEMORY_DISK_Thread.start()

    network_handler()
    system_handler()


def FIRST_SETUP():
    """
    This function handles the initinal data. First it does the key exchange, then opens the GUI and then checking with
    the server the existence of the computer. In the case that the computer does exist, this function will over and move
    on to the next function (main()) and in the case the computer does not exist, the fucntion will send some initinal
    data to the server and then will keep going to the next function.
    :return:
    """
    global gui

    # Recives server's RSA public key
    comm.sec.server_public_key = Security.import_key(comm.sock.recv(1024))
    # Sends AES key, mode and iv to the server
    comm.sock.send(cPickle.dumps([comm.sec.aes_key, comm.sec.mode, comm.sec.iv]))

    # Initilizes the GUI. The target function is user_handle() which means that this function will get the user inputs
    # After the user entered correct username and password the code will continue
    gui.run(user_handle)

    # Gets computer UUID
    UUID = s.get_computer_UUID()
    # Sends computer UUID to the server (Table: Computer | Colunm: Computer-ID)
    comm.send(["Computer", "Computer-ID", UUID])

    # Recives data from the server if the computer does exist in the database
    if_computer_exist = comm.recv()
    print if_computer_exist
    if if_computer_exist == response.OK_200:
        return

    # From now on until the 'return' statment, the client will be sending initinal data about the computer:
    # 1. Computer operation system
    # 2. CPU model
    # 3. How many CPU the computer has
    # 4. Total memory ram

    OS_version = s.get_os_version()
    comm.send(["Computer", "OS_version", OS_version])

    CPU_model = c.get_cpu_model()
    comm.send(["System", "CPU_model", CPU_model])

    CPU_num = c.get_cpu_num()
    comm.send(["System", "CPU_num", CPU_num])

    Memo_Total_Ram = m.memory_ram()[default.ZERO]
    comm.send(["System", "Memo_Total_Ram", Memo_Total_Ram])

    # -- The server is ready to get the rest of the data data from the client -- #
    return


if __name__ == "__main__":
    FIRST_SETUP()
    main()
