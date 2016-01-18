import win32api
import ctypes
from Config import *

drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\000')[:-1]
print [unicode(d) for d in drives]

freeuser = ctypes.c_int64()
total = ctypes.c_int64()
free = ctypes.c_int64()

for i in range(2):
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(u'C:\\', ctypes.byref(freeuser), ctypes.byref(free), ctypes.byref(total))
    print bytes2human(free.value)
