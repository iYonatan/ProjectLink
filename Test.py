import win32com
from win32com.client import GetObject

wmi = win32com.client.GetObject("winmgmts:")
wmi = win32com.client.gencache.EnsureDispatch(wmi._oleobj_)
# Now execute your query
process = wmi.ExecQuery('select * from Win32_Process')
proc = process[0]
# Now I can do things like check properties
print proc.Properties_('ProcessId').Value
