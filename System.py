# TODO: Every error message, must be declered in the config file (config.py)
# TODO: Declare (in config.py) the meaning of: callback, registry

from Config import *

import _winreg
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
# TODO: CPU Utilization, Process cpu usage

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

c = CPU()
print "# ============================================================================ # CPU"
print c.get_cpu_model()

# ============================================================================ Memory

# ============================================================================ Disk

# ============================================================================ Network
