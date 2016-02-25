import _winreg

SLEEP_TIME_1 = 1
SLEEP_TIME_1_5 = 1.5
PERCENT_LIMIT = 100


def bytes2human(n):
    """
    Converts bytes to a readble number
    :param n: A number in bytes
    :return: Readble number with units (KB, MB ....) (string)
    """

    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def bytes2percent(smaller_num, bigger_num):
    """
    Converts bytes to percents
    :param smaller_num: Smaller number
    :param bigger_num: Bigger number
    :return: The perecentege between the numbers
    """
    try:
        return int(round(smaller_num / float(bigger_num), 2) * 100)
    except:
        return 0


def get_registry_value(key, subkey, value):
    """
    Finds a value from the registry editor in windows
    :param key: (HKEY_CLASSES_ROOT | HKEY_CURRENT_USER | HKEY_LOCAL_MACHINE | HKEY_USERS | HKEY_CURRENT_CONFIG)
    :param subkey: The folders under param: key
    :param value: The filed that we want to find its value
    :return: value of param: value
    """

    key = getattr(_winreg, key)
    handle = _winreg.OpenKey(key, subkey)
    (value, type) = _winreg.QueryValueEx(handle, value)
    return value
