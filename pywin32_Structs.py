from ctypes import *
from ctypes.wintypes import *

# ============================================================================ GLABAL VARS

# -- DLL --
KERNEL_32 = windll.Kernel32

# -- Security --
ALL_PROCESS_ACCESS = (0x000F0000L | 0x00100000L | 0xFFF)

# -- Vars --
SIZE_T = c_size_t


# ============================================================================ CPU
class FILETIME(Structure):
    _fields_ = [
        ("dwLowDateTime", DWORD),
        ("dwHighDateTime", DWORD)]


# ============================================================================ Memory
class MEMORYSTATUSEX(Structure):
    _fields_ = [
        ("dwLength", c_ulong),
        ("dwMemoryLoad", c_ulong),
        ("ullTotalPhys", c_ulonglong),
        ("ullAvailPhys", c_ulonglong),
        ("ullTotalPageFile", c_ulonglong),
        ("ullAvailPageFile", c_ulonglong),
        ("ullTotalVirtual", c_ulonglong),
        ("ullAvailVirtual", c_ulonglong),
        ("sullAvailExtendedVirtual", c_ulonglong),
    ]


class PROCESS_MEMORY_COUNTERS_EX(Structure):
    _fields_ = [
        ('cb', DWORD),
        ('PageFaultCount', DWORD),
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
