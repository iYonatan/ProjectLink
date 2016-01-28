# TODO: Every error message and numbers, must be declered in the config file (config.py)
# TODO: Declare in the config file the meaning of: callback and registry

import ctypes
import time
import win32api
import win32pdh
import win32process

import socket
import struct

from functions import *
from pywin32_Structs import *

proc = ctypes.windll.Kernel32.OpenProcess(ALL_PROCESS_ACCESS, False, 2376)


# ============================================================================ System
# TODO: Done!

class System:
    def __init__(self):
        pass

    def get_os_version(self):
        """
        By using the regisry, we export the operation system's version
        :return: value (string)
        """

        return get_registry_value(
                "HKEY_LOCAL_MACHINE",
                "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
                "ProductName")

    def get_processes_list(self):
        """
        returns a processes list which are running right now on the computer
        :return: proc_list (list)
        """

        try:
            junk, proc_list = win32pdh.EnumObjectItems(None, None, 'process', win32pdh.PERF_DETAIL_WIZARD)
            return junk
        except:
            try:
                from win32com.client import GetObject
                WMI = GetObject('winmgmts:')  # COM object
                proc_instances = WMI.InstancesOf('Win32_Process')  # WMI instanse
                proc_list = [process.Properties_('Name').Value for process in
                             proc_instances]  # Get the processess names
                return proc_list
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
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
                titles.append(buff.value)
            return True

        EnumWindows(EnumWindowsProc(foreach_window), 0)  # Callback
        return titles


s = System()
print "# ============================================================================ # System"
print s.get_os_version()


# ============================================================================ CPU
# TODO: (?) Make a dll for the function GetSystemTimes() and cpu_process_util()


def GetSystemTimes():
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


class CPU:
    def __init__(self):
        self.sys = None

    def get_cpu_model(self):
        """
        Return the CPU model
        :return: CPU model (string)
        """
        return get_registry_value(
                "HKEY_LOCAL_MACHINE",
                "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
                "ProcessorNameString")

    def cpu_utilization(self):
        """
        Returns the total cpu usage

        Source: http://www.codeproject.com/Articles/9113/Get-CPU-Usage-with-GetSystemTimes
        :return: CPU usage (int)
        """

        FirstSystemTimes = GetSystemTimes()
        time.sleep(SLEEP_TIME_1_5)
        SecSystemTimes = GetSystemTimes()

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
        return int((self.sys - idl) * 100 / self.sys)

    def cpu_process_util(self, hproc):
        """
        Returns the process usage of CPU

        Source: http://www.philosophicalgeek.com/2009/01/03/determine-cpu-usage-of-current-process-c-and-c/
        :param hproc: Process handle
        :return: Process CPU usage (int)
        """

        FirstProcessTimes = win32process.GetProcessTimes(hproc)
        time.sleep(SLEEP_TIME_1_5)
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

        return (100 * proc_total_time) / self.sys


c = CPU()
print "# ============================================================================ # CPU"
print c.cpu_utilization()


# ============================================================================ Memory
class Memory:
    def __init__(self):
        pass

    def memory_ram(self):
        """
        Returning the total and the free amount of ram
        :return: total and the availabe ram (int tuple)
        """
        memoryStatus = MEMORYSTATUSEX()
        memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        KERNEL_32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))
        return memoryStatus.ullTotalPhys, memoryStatus.ullAvailPhys

    def memory_process_usage(self, hproc):
        """Return Win32 process memory counters structure as a dict.
        :param hproc: Process handle
        :returns
        """
        GetProcessMemoryInfo = ctypes.windll.psapi.GetProcessMemoryInfo
        counters = PROCESS_MEMORY_COUNTERS_EX()

        ret = GetProcessMemoryInfo(hproc, ctypes.byref(counters),
                                   ctypes.sizeof(counters))
        if not ret:
            raise ctypes.WinError()

        return counters.WorkingSetSize


m = Memory()
print "# ============================================================================ # Memory"
print [bytes2human(ram) for ram in m.memory_ram()]


# ============================================================================ Disk
# TODO: Done!


class Disk:
    def __init__(self):
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
            drive = unicode(drive)
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
            GetDiskFreeSpaceExW(drive, ctypes.byref(freeuser), ctypes.byref(total), ctypes.byref(free))
            self.disk_dict[drive] = {'total': bytes2human(total.value),
                                     'free': bytes2human(free.value)}


d = Disk()
print "# ============================================================================ # Disk"
print d.disk_dict


# ============================================================================ Network
# TODO: Packet sniffer for: IP, TCP, UDP, ICMP, FTP


class Network:
    def __init__(self):
        pass

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

        return version, ttl, proto, self.get_ipv4_addr(src), self.get_ipv4_addr(target), data[20:]

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

        TAB_1 = '\t - '
        TAB_2 = '\t\t - '
        TAB_3 = '\t\t\t - '

        # TODO: Gets computer's ip through the config file

        conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        conn.bind(("10.92.5.59", 0))

        # Include IP headers
        conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # receive all packages
        conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        print "Continue...."

        while True:
            raw_data, addr = conn.recvfrom(65535)

            version, ttl, proto, src, dest, data = self.IPv4_packet(raw_data)
            print('\nIP Packet:')
            print('Version: {}, Destination: {}, Source: {}, Next Protocol: {}'.format(version, dest, src, proto))

            if proto == 1:
                (icmp_type, code, checksum, data) = self.ICMP_packet(data)
                print TAB_1 + "ICMP Packet:"
                print (TAB_2 + 'icmp_type: {}, code: {}, checksum: {}'.format(icmp_type, code, checksum, data))

            elif proto == 6:
                (src_port, dest_port, sequence, ack,
                 flag_urg,
                 flag_ack,
                 flag_psh,
                 flag_rst,
                 flag_syn,
                 flag_fin,
                 data) = self.TCP_segment(data)

                print TAB_1 + "TCP segment:"
                print (TAB_2 + 'src_port: {}, dest_port: {}'.format(src_port, dest_port, ))
                print (
                    TAB_3 + 'flag_urg: {}, flag_ack: {}, flag_psh: {},flag_rst: {}, flag_syn: {}, flag_fin: {}'.format(
                            flag_urg,
                            flag_ack,
                            flag_psh,
                            flag_rst,
                            flag_syn,
                            flag_fin))

            elif proto == 17:
                (src_port, dest_port, length, data) = self.UDP_segment(data)
                print TAB_1 + "UDP segment:"
                print (TAB_2 + 'Source Port: {}, Destination Port: {}, Length: {}'.format(src_port, dest_port, length))

            else:
                print(TAB_1 + 'Other IPv4 Data...')


n = Network()
print "# ============================================================================ # Network"
n.run()
