import time
from functions import *


class Monitor(object):
    def __init__(self, comm):
        self.comm = comm
        self.segments = []  # Collects the segments
        self.segments_dict = {}

        self.suspicious_processes = []
        self.disk = {}

    def cpu_warning(self, hcpu, proc):
        """
        Seeing a process if suspicious or not.
        This function is ivoked when a sepcific process usage is up to 20%

        :param hcpu: CPU() instance
        :param proc: process handler
        :return: if suspicious (Boolean) and process handler (hprocess)
        """
        start = time.time()

        pid = proc.keys()[0]
        name_proc = proc[pid][0]
        handle_proc = proc[pid][1]

        while True:
            time.sleep(1)
            try:
                usage = hcpu.cpu_process_util(handle_proc)
            except:
                return False, None
            if usage < 20:
                return False, usage

            now = time.time()

            if (now - start) > 20:
                self.suspicious_processes.append(name_proc)
                self.comm.send(
                    "(CPU) Suspicious process has been found: {} (PID: {}) has {}%".format(str(name_proc), str(pid),
                                                                                           str(usage)))
                return True, usage

    def memory_warning(self, hmemo, proc, used):
        """
        Seeing a process if suspicious or not.
        This function is ivoked when a sepcific process memory usage is up to 10%

        :param used: The used memory in percent
        :param hmemo: Memory() instance
        :param proc: process handler
        :return: if suspicious (Boolean) and process handler (hprocess)
        """
        start = time.time()

        pid = proc.keys()[0]
        name_proc = proc[pid][0]
        handle_proc = proc[pid][1]

        while True:
            time.sleep(1)
            try:
                proc_usage = bytes2percent(hmemo.memory_process_usage(handle_proc), used)
            except:
                return False, None
            if proc_usage <= 10:
                return False, proc_usage

            now = time.time()

            if (now - start) >= 20:
                self.suspicious_processes.append(name_proc)
                self.comm.send("(Memory) Suspicious process has been found: {} (PID: {}) has {}%".format(str(name_proc),
                                                                                                         str(pid),
                                                                                                         str(proc_usage)
                                                                                                         ))
                return True, proc_usage

    def disk_warning(self, disk_dict):
        for key, disk_data in disk_dict.items():
            disk_used_percent = bytes2percent(disk_data['used'], disk_data['total'])

            if disk_used_percent >= 50 and disk_used_percent > self.disk[key]:
                self.disk[key] = disk_used_percent
                print "{} is {}% full".format(key, str(disk_used_percent))

        return

    def Add_segmnet(self, segment):
        """
        Adds a segment to self.segments
        :param segment: A segment (dict)
        :return: None
        """
        self.segments.append(segment)

    def Network_warning(self):
        # TODO: make a code for UDP flood
        """
        Seeing for DDOS attack in TCP (SYN flood)
        :return: None
        """
        main_segment = {}

        while True:
            for segment in self.segments:
                main_segment = segment
                if not self.segments_dict.has_key(segment['dest_port']):
                    self.segments_dict[segment['dest_port']] = [int()]
                    self.segments_dict[segment['dest_port']].append(time.time())
                else:
                    self.segments.remove(segment)
                    break

                self.segments.remove(segment)

            try:
                self.segments_dict[main_segment['dest_port']][0] += 1
                # print "segment: {} || Counter is: {}".format(str(main_segment),
                #                                              str(self.segments_dict[main_segment['dest_port']]))
                src_ip = main_segment['src_ip']
                main_segment = {}
                now = time.time()
                for key, value in self.segments_dict.items():
                    if value[0] % 100 == 0:  # Number of packets in a particular port
                        if now - value[1] < 3:
                            print "DDOS ATTACK!! From: {}".format(src_ip)

                        else:
                            value[1] = time.time()

            except:
                main_segment = {}
