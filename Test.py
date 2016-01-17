"""Functions for getting memory usage of Windows processes."""
import time
from Config import *


import ctypes
from ctypes import wintypes


SIZE_T = ctypes.c_size_t
ALL_PROCESS_ACCESS = (0x000F0000L | 0x00100000L | 0xFFF)


class PROCESS_MEMORY_COUNTERS_EX(ctypes.Structure):
    _fields_ = [
        ('cb', wintypes.DWORD),
        ('PageFaultCount', wintypes.DWORD),
        ('PeakWorkingSetSize', SIZE_T),
        ('WorkingSetSize', SIZE_T),
        ('QuotaPeakPagedPoolUsage', SIZE_T),
        ('QuotaPagedPoolUsage', SIZE_T),
        ('QuotaPeakNonPagedPoolUsage', SIZE_T),
        ('QuotaNonPagedPoolUsage', SIZE_T),
        ('PagefileUsage', SIZE_T),
        ('PeakPagefileUsage', SIZE_T),
        ('PrivateUsage', SIZE_T),
    ]


GetProcessMemoryInfo = ctypes.windll.psapi.GetProcessMemoryInfo


def get_memory_info(process=None):
    """Return Win32 process memory counters structure as a dict.
    :param process: Process handle
    :returns
    """
    counters = PROCESS_MEMORY_COUNTERS_EX()
    ret = GetProcessMemoryInfo(process, ctypes.byref(counters),
                               ctypes.sizeof(counters))
    if not ret:
        raise ctypes.WinError()

    return counters.WorkingSetSize



if __name__ == '__main__':
    proc = ctypes.windll.Kernel32.OpenProcess(ALL_PROCESS_ACCESS, False, 13840)

    import pprint

    while 1:
        pprint.pprint((get_memory_info(proc))/1024)
        time.sleep(2)
