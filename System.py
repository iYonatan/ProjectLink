# TODO: Every error message, must be declered in the config file (config.py)
# TODO: Declare (in config.py) the meaning of: callback, registry


from Config import *
from pywin32_Structs import *

from ctypes import windll, byref

import time
import ctypes
import win32pdh


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
# TODO: Process cpu usage


def GetSystemTimes():
    """
    Uses the function GetSystemTimes() (win32) in order to get the user time, kernel time and idle time
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
        pass

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
        Calculates the CPU utilization by GetSystemTimes() function from win32 api.
        The calculation includes: User mode time, Kernel mode time and Idle mode time.

        Source: http://www.codeproject.com/Articles/9113/Get-CPU-Usage-with-GetSystemTimes
        :return: CPU usage (int)
        """

        FirstSystemTimes = GetSystemTimes()
        time.sleep(1.5)
        SecSystemTimes = GetSystemTimes()

        usr = SecSystemTimes['userTime'] - FirstSystemTimes['userTime']
        ker = SecSystemTimes['kernelTime'] - FirstSystemTimes['kernelTime']
        idl = SecSystemTimes['idleTime'] - FirstSystemTimes['idleTime']

        sys = usr + ker

        return int((sys - idl) * 100 / sys)

    def cpu_process_util(self):
        import win32process
        d = win32process.GetProcessTimes(win32process.GetCurrentProcess())
        return (d['UserTime'] / 1e7,
                d['KernelTime'] / 1e7)


c = CPU()
print "# ============================================================================ # CPU"
# while 1:
#     print str(c.cpu_utilization()) + '%'
#     print str(c.cpu_utilization()) + '%'
#     print "--------------"
print c.cpu_process_util()

# ============================================================================ Memory

# ============================================================================ Disk

# ============================================================================ Network

# ============================================================================ Tests
