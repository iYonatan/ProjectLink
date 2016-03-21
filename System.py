# TODO: Every error message and numbers, must be declered in the config file (config.py)
# TODO: Declare in the config file the meaning of: callback and registry

from subprocess import Popen, PIPE
import ctypes
import time
import win32api
import win32pdh
import win32process
import multiprocessing

import socket
import struct

from config import *
from functions import *
from pywin32_Structs import *


# proc = ctypes.windll.Kernel32.OpenProcess(ALL_PROCESS_ACCESS, False, 14436)

# ============================================================================ System

class System:
    def __init__(self):
        self.processes = {}
        self.obj = 'process'
        self.item = 'ID Process'

    def get_os_version(self):
        """
        By using the regisry, we export the operation system's version
        :return: value (string)
        """

        return get_registry_value(
            "HKEY_LOCAL_MACHINE",
            "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
            "ProductName")

    def get_computer_name(self):
        return win32api.GetUserName()

    def get_computer_UUID(self):
        uuid = Popen(['wmic', 'csproduct', 'get', 'UUID'], stdout=PIPE, stdin=PIPE)
        return uuid.communicate()[default.ZERO].split()[default.ONE]

    def get_processes_dict(self):
        """
        returns an ID processes lis
        :return: proc_handle (list)
        """

        try:
            # Getting all processes name
            junk, proc_name = win32pdh.EnumObjectItems(None, None, self.obj, win32pdh.PERF_DETAIL_WIZARD)

            instances = {}

            for instance in proc_name:
                if instance in instances:
                    instances[instance] += default.ONE
                else:
                    instances[instance] = default.ZERO

            proc_pid_name = {}

            for instance, max_instances in instances.items():
                for inum in xrange(max_instances + default.ONE):
                    try:
                        hq = win32pdh.OpenQuery()  # initializes the query handle
                        path = win32pdh.MakeCounterPath((None, self.obj, instance, None, inum, self.item))
                        counter_handle = win32pdh.AddCounter(hq, path)  # convert counter path to counter handle
                        win32pdh.CollectQueryData(hq)  # collects data for the counter
                        type, val = win32pdh.GetFormattedCounterValue(counter_handle, win32pdh.PDH_FMT_LONG)

                        proc_pid_name[val] = [instance]

                        win32pdh.CloseQuery(hq)
                    except:
                        raise OSError("Problem getting process id")

            return proc_pid_name

        except:
            try:
                from win32com.client import GetObject
                WMI = GetObject('winmgmts:')  # COM object
                proc_instances = WMI.InstancesOf('Win32_Process')  # WMI instanse

                proc_name = [process.Properties_('Name').Value for process in
                             proc_instances]  # Get the processess names

                proc_id = [process.Properties_('ProcessId').Value for process in
                           proc_instances]  # Get the processess names

                proc_pid_name = {}

                proc_id_counter = default.ZERO
                for instance in range(len(proc_name)):
                    proc_pid_name[proc_id[instance]] = [(proc_name[instance])]
                    proc_id_counter += default.ONE

                return proc_pid_name

            except:
                raise OSError('Counldn\'t get the process list')

    def get_windows(self):
        """
        Return a list which contains the opened windows titles.
        :return: title (list)
        """

        EnumWindows = ctypes.windll.user32.EnumWindows  # Filters all toplevel(opened) windows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int),
                                             ctypes.POINTER(ctypes.c_int))  # Callback function. Returns a tuple
        GetWindowText = ctypes.windll.user32.GetWindowTextW  # Gets window's title
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW  # Gets the exacly buffer size of the title
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible  # Filters all the visible windows

        titles = []

        def foreach_window(hwnd, lParam):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                buff = ctypes.create_unicode_buffer(length + default.ONE)
                GetWindowText(hwnd, buff, length + default.ONE)
                titles.append(buff.value)
            return True

        EnumWindows(EnumWindowsProc(foreach_window), default.ZERO)  # Callback
        return titles

    def create_process_handle_dict(self, procsses):
        """
        Creates a dictinary of process handle
        :param procsses:
        :return: None
        """
        for pid in procsses:
            proc_handle = ctypes.windll.Kernel32.OpenProcess(ALL_PROCESS_ACCESS, False, pid)
            procsses[pid].append(proc_handle)

    def close_process_handle(self, hproc):
        """
        Closes a given process handle
        :param hproc: process handle
        :return: None
        """
        ctypes.windll.Kernel32.CloseHandle(hproc)
        return

    def run(self):
        """
        Runs System class
        :return:
        """
        new_pid_dict = self.get_processes_dict()

        if not new_pid_dict:
            return

        new_processes = set(new_pid_dict) - set(self.processes)
        closed_processes = set(self.processes) - set(new_pid_dict)

        new_processes_dict = {}
        closed_processes_dict = {}

        if len(new_processes) > default.ZERO:
            self.create_process_handle_dict(new_pid_dict)
            for pid in new_processes:
                if new_pid_dict[pid][default.ZERO] is 0:
                    continue
                self.processes.update({pid: new_pid_dict[pid]})
                new_processes_dict.update({pid: new_pid_dict[pid]})

        if len(closed_processes) > default.ZERO:
            for pid in closed_processes:
                closed_processes_dict.update({pid: self.processes[pid]})
                self.close_process_handle(self.processes[pid][1])
                self.processes[pid][1] = 0  # The place of 1 is the process handle
                self.processes.pop(pid, None)

        return new_processes_dict, closed_processes_dict


# ============================================================================ CPU

class CPU:
    def __init__(self, monitor):
        self.sys = None
        self.monitor = monitor

    def get_cpu_model(self):
        """
        Return the CPU model
        :return: CPU model (string)
        """
        return get_registry_value(
            "HKEY_LOCAL_MACHINE",
            "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
            "ProcessorNameString")

    def get_cpu_num(self):
        return multiprocessing.cpu_count()

    def GetSystemTimes(self):
        # TODO: (?) Make a dll for the function GetSystemTimes() and cpu_process_util()
        """
        Uses the function GetSystemTimes() (win32) in order to get the user mode time, kernel mode time and idle mode time
        :return: user time, kernel time and idle time (Dictinary)
        """

        __GetSystemTimes = windll.kernel32.GetSystemTimes
        idleTime, kernelTime, userTime = FILETIME(), FILETIME(), FILETIME()

        success = __GetSystemTimes(

            byref(idleTime),
            byref(kernelTime),
            byref(userTime))

        assert success, ctypes.WinError(ctypes.GetLastError())[1]

        return {
            "idleTime": idleTime.dwLowDateTime,
            "kernelTime": kernelTime.dwLowDateTime,
            "userTime": userTime.dwLowDateTime}

    def cpu_utilization(self):
        """
        Returns the total cpu usage

        Source: http://www.codeproject.com/Articles/9113/Get-CPU-Usage-with-GetSystemTimes
        :return: CPU usage (int)
        """

        FirstSystemTimes = self.GetSystemTimes()
        time.sleep(1)
        SecSystemTimes = self.GetSystemTimes()

        """
         CPU usage is calculated by getting the total amount of time
         the system has operated since the last measurement
         made up of kernel + user) and the total
         amount of time the process has run (kernel + user).
        """

        usr = SecSystemTimes['userTime'] - FirstSystemTimes['userTime']
        ker = SecSystemTimes['kernelTime'] - FirstSystemTimes['kernelTime']
        idl = SecSystemTimes['idleTime'] - FirstSystemTimes['idleTime']
        self.sys = usr + ker
        return int((self.sys - idl) * default.PERCENT_LIMIT / self.sys)

    def cpu_process_util(self, hproc):
        """
        Returns the process usage of CPU
        ** self.cpu_utilization() must run first!!
        Source: http://www.philosophicalgeek.com/2009/01/03/determine-cpu-usage-of-current-process-c-and-c/
        :param hproc: Process handle
        :return: Process CPU usage (int)
        """

        # hproc = proc

        FirstProcessTimes = win32process.GetProcessTimes(hproc)
        time.sleep(1)
        SecProcessTimes = win32process.GetProcessTimes(hproc)

        """
         Process CPU usage is calculated by getting the total amount of time
         the system has operated since the last measurement
         made up of kernel + user) and the total
         amount of time the process has run (kernel + user).
        """

        proc_time_user_prev = FirstProcessTimes['UserTime']
        proc_time_kernel_prev = FirstProcessTimes['KernelTime']

        proc_time_user = SecProcessTimes['UserTime']
        proc_time_kernel = SecProcessTimes['KernelTime']

        proc_usr = proc_time_user - proc_time_user_prev
        proc_ker = proc_time_kernel - proc_time_kernel_prev

        proc_total_time = proc_usr + proc_ker

        proc_utilization = (default.PERCENT_LIMIT * proc_total_time) / self.sys
        return proc_utilization

    def run(self, proc):
        """
        Runs CPU class
        :param proc: A process dictinary (dict)
        :return:
        """

        pid = proc.keys()[default.ZERO]
        handle_proc = proc[pid][system.PROCESS_HANDLE]
        while True:
            time.sleep(default.ONE)

            if handle_proc == default.ZERO:
                return

            cpu_usage = self.cpu_utilization()
            if cpu_usage > system.NORMAL_CPU_USAGE:
                try:
                    process_usage = self.cpu_process_util(handle_proc)
                except:
                    break
                if process_usage > system.NORAML_PROCESS_USAGE:
                    suspicious = self.monitor.cpu_warning(self, proc)
                    if not suspicious[default.ZERO]:
                        continue
            time.sleep(10)


# ============================================================================ Memory


class Memory:
    def __init__(self, monitor):
        self.monitor = monitor

    def memory_ram(self):
        """
        Returning the total and the free amount of ram
        :return: total and the availabe ram (int tuple)
        """
        memoryStatus = MEMORYSTATUSEX()
        memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        KERNEL_32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))
        return memoryStatus.ullTotalPhys, memoryStatus.ullAvailPhys

    def memory_utilization(self):
        (Total, Avail) = self.memory_ram()
        return bytes2percent(Avail, Total)

    def memory_process_usage(self, hproc):
        """
        Return Win32 process memory counters structure as a dict.
        :param hproc: Process handle
        :returns WorkingSetSize of memory (int)
        """
        GetProcessMemoryInfo = ctypes.windll.psapi.GetProcessMemoryInfo
        counters = PROCESS_MEMORY_COUNTERS_EX()

        ret = GetProcessMemoryInfo(hproc, ctypes.byref(counters),
                                   ctypes.sizeof(counters))
        if not ret:
            raise ctypes.WinError()

        return counters.WorkingSetSize

    def run(self, proc):
        """
        Runs the class
        :param proc: process dictinary (dict)
        :return: None
        """
        total = self.memory_ram()[default.ZERO]

        pid = proc.keys()[default.ZERO]
        handle_proc = proc[pid][system.PROCESS_HANDLE]

        while default.UNLIMITED_LOOP:
            if handle_proc == default.ZERO:
                return
            avail = self.memory_ram()[default.ONE]
            used = total - avail
            used_usage = bytes2percent(used, total)
            if used_usage > 40:
                try:
                    proc_usage = bytes2percent(self.memory_process_usage(handle_proc), used)
                except:
                    break
                if proc_usage >= 10:
                    suspicious = self.monitor.memory_warning(self, proc, used)
                    if not suspicious[default.ZERO]:
                        continue
            time.sleep(10)


# ============================================================================ Disk

class Disk:
    # TODO: Get Installed applocations list names and size (the size is in bytes)

    def __init__(self, monitor):
        self.monitor = monitor

        self.disk_dict = {}
        self.disk_get_partitions()
        self.disk_usage()

    def disk_get_partitions(self):
        """
        Fills the keys of self.disk_dict.
        The keys are the devices which connected to the computer.

        :return: None
        """
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        for drive in drives:
            self.disk_dict[drive] = {}

    def disk_usage(self):
        """
        Getting information about every device in self.disk_dict.
        :return: None
        """
        freeuser = ctypes.c_int64()
        total = ctypes.c_int64()
        free = ctypes.c_int64()
        for drive in self.disk_dict:
            GetDiskFreeSpaceExW(unicode(drive), ctypes.byref(freeuser), ctypes.byref(total), ctypes.byref(free))
            self.disk_dict[drive] = {'total': total.value,
                                     'used': (total.value - free.value)}

    def run(self):
        """
        Runs Disk class
        :return:
        """
        self.monitor.disk = dict.fromkeys(self.disk_dict)
        while True:
            self.monitor.disk_warning(self.disk_dict)
            time.sleep(1800)  # 30 minutes


# ============================================================================ Network

class Network:
    def __init__(self, monitor):

        self.monitor = monitor

        self.IP_ADDR = "10.92.5.59"

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

        self.conn.bind((self.IP_ADDR, 0))

        # Include IP headers
        self.conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, default.ONE)

        # receive all packages
        self.conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def get_ipv4_addr(self, bytes_addr):
        """
        Returns a readble ipv4 from bytes (X.X.X.X)
        :param bytes_addr: IP address in bytes
        :return: readble ipv4 (string)
        """
        return socket.inet_ntoa(bytes_addr)

    def IPv4_packet(self, data):
        """
        Extracts IPV4 packet
        :param data: A packet (Bytes)
        :return: version, ttl, protocol, src, target and the rest of the data
        """
        version_header_length, ttl, proto, src, target = struct.unpack('! B 7x B B 2x 4s 4s', data[:20])

        version = version_header_length >> 4
        header_length = (version_header_length & 15) * 4

        return version, ttl, proto, self.get_ipv4_addr(src), self.get_ipv4_addr(target), data[header_length:]

    def ICMP_packet(self, data):
        """
        Extracts ICMP packet
        :param data: A packet (Bytes)
        :return: icmp_type, code and checksum
        """
        icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
        return icmp_type, code, checksum, data[4:]

    def TCP_segment(self, data):
        """
        Extracts TCP segment
        :param data: A segment (Bytes)
        :return: source port, destenation port, sequence number, acknowledgment number and all flags
        """
        (src_port, dest_port, sequence, ack, offset_reserved_flags) = struct.unpack('! H H L L H', data[:14])
        offset = (offset_reserved_flags >> 12) * 4

        flag_urg = (offset_reserved_flags & 32) >> 5
        flag_ack = (offset_reserved_flags & 16) >> 4
        flag_psh = (offset_reserved_flags & 8) >> 3
        flag_rst = (offset_reserved_flags & 4) >> 2
        flag_syn = (offset_reserved_flags & 2) >> 1
        flag_fin = (offset_reserved_flags & 1)

        return src_port, dest_port, sequence, ack, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[
                                                                                                               offset:]

    def UDP_segment(self, data):
        """
        Extracts UDP segment
        :param data: A segment (Bytes)
        :return: source port, destenation port, checksum and the rest data
        """
        (src_port, dest_port, checksum) = struct.unpack('! H H 2x H', data[:8])
        return src_port, dest_port, checksum, data[8:]

    def run(self):
        """
        Runs Network class
        :return:
        """
        # TODO: Gets computer's ip through the config file

        while default.UNLIMITED_LOOP:
            raw_data, addr = self.conn.recvfrom(network.MAX_PACKET_RECIVER)

            version, ttl, proto, src, dest, data = self.IPv4_packet(raw_data)
            # # region Print
            # print('\nIP Packet:')
            # print('Version: {}, Destination: {}, Source: {}, Next Protocol: {}'.format(version, dest, src, proto))
            # # endregion

            # ICMP pakcet
            if proto == network.ICMP:
                (icmp_type, code, checksum, data) = self.ICMP_packet(data)
                # # region Print
                # print TAB_1 + "ICMP Packet:"
                # print (TAB_2 + 'icmp_type: {}, code: {}, checksum: {}'.format(icmp_type, code, checksum, data))
                # # endregion

            # TCP segment
            elif proto == network.TCP:

                (src_port, dest_port, sequence, ack,
                 flag_urg,
                 flag_ack,
                 flag_psh,
                 flag_rst,
                 flag_syn,
                 flag_fin,
                 data) = self.TCP_segment(data)

                flags = {"urg": flag_urg,
                         "ack": flag_ack,
                         "psh": flag_psh,
                         "rst": flag_rst,
                         "syn": flag_syn,
                         "fin": flag_fin}

                only_syn = sum(int(v) for k, v in flags.iteritems() if k != "syn") == 0 and flags["syn"] != 0

                tcp_segment = {
                    "src_ip": src,
                    "dest_ip": dest,
                    "src_port": src_port,
                    "dest_port": dest_port,
                    "flag_syn": flag_syn,
                }

                if only_syn and tcp_segment["src_ip"] != self.IP_ADDR:
                    self.monitor.Add_segmnet(tcp_segment)
                    # print tcp_segment
                    # # region Print
                    # "TCP segment:"

                    # print ('src_port: {}, dest_port: {}'.format(src_port, dest_port, ))
                    # print (
                    #     'flag_urg: {}, flag_ack: {}, flag_psh: {},flag_rst: {}, flag_syn: {}, flag_fin: {}'.format(
                    #         flag_urg,
                    #         flag_ack,
                    #         flag_psh,
                    #         flag_rst,
                    #         flag_syn,
                    #         flag_fin))
                    # # endregion

            # UDP segment
            elif proto == network.UDP:
                (src_port, dest_port, length, data) = self.UDP_segment(data)
                # # region Print
                # print TAB_1 + "UDP segment:"
                # print ('Source Port: {}, Destination Port: {}, Length: {}'.format(src_port, dest_port, length))
                # # endregion

            else:
                continue
                # print(TAB_1 + 'Other IPv4 Data...')
