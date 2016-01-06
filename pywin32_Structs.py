from ctypes import *
from ctypes.wintypes import *


# ============================================================================ CPU
class FILETIME(Structure):
    _fields_ = [
        ("dwLowDateTime", DWORD),
        ("dwHighDateTime", DWORD)]
