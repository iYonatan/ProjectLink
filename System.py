# TODO: Every error message and numbers, must be declered in the config file (config.py)
# TODO: Declare in the config file the meaning of: callback and registry

import ctypes
import time
import win32api
import win32pdh
import win32process

from Config import *
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
# TODO: Packet sniffer for: Ethernet, IP, TCP, ICMP, HTTP, FTP


class Network:
    def __init__(self):
        pass

n = Network()
print "# ============================================================================ # Network"
# ============================================================================ Tests
