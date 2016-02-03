import time


class Monitor(object):
    def __init__(self):
        self.segments = []  # Collects the segments
        # Declare a specific segment for checking if the other segments have the same dest port in short time
        self.main_segment = None
        self.suspicious_segment_counter = 0
        self.suspicious_segments = []

        self.suspicious_processes = []

    def cpu_warning(self, hcpu, hproc):
        """
        Seeing a process if suspicious or not.
        This function is ivoked when a sepcific process usage is up to 20%

        :param hcpu: CPU() handler
        :param hproc: process handler
        :return: if suspicious (Boolean) and process handler (hprocess)
        """
        start = time.time()
        while True:
            usage = hcpu.cpu_process_util(hproc)

            if usage < 20:
                return False, usage

            now = time.time()

            if (now - start) > 20:
                self.suspicious_processes.append(hproc)
                print "Suspicious process has been found: {} has {}%".format(str(hproc), str(usage))
                return True, usage

    def memory_warning(self):
        pass

    def disk_warning(self):
        pass

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
        Seeing for DDOS attack in TCP and UDP
        :return: None
        """
        start_suspicious_time = None
        passed_it = True

        while True:
            for segment in self.segments:

                # TODO: Check if the source IP is not the local coputer's ID
                if (segment['flag_syn'] is 1) and passed_it:
                    start_suspicious_time = time.time()  # Starts counting the time
                    self.main_segment = segment  # Saves the segment
                    passed_it = False  # Ensures that the program wont repeat this condition again

                else:

                    # TCP DDOS attack testing
                    if (segment['flag_syn'] is 1) and (segment['dest_port'] == self.main_segment['dest_port']):
                        self.suspicious_segment_counter += 1  # Increased by 1
                        self.suspicious_segments.append(segment)  # Adding to the list
                        # print "Flag syn is 1 and destination port is the same"
                        # print self.main_segment['dest_port']
                        # print segment

                        # If 500 packets have been found ...
                        if self.suspicious_segment_counter >= 500:
                            end_suspicious_time = time.time()  # Stops the time
                            critic_time = round(end_suspicious_time - start_suspicious_time)  # In seconds
                            # print "suspicious_segment_counter >= 500"

                            # If the sub of the time since the first packe until now is between 2 to 3 ...
                            if (2 < critic_time < 3) and (all(segment == self.main_segment['src_ip'] for segment in
                                                              self.suspicious_segments)):
                                print "DDOS Attack! wake up!!!!"

                            elif critic_time < 1:
                                print "DDOS Attack! wake up!!!!"

                            else:
                                self.suspicious_segments = []  # Reset
                                self.suspicious_segment_counter = 0  # Reset
                                passed_it = True  # Reset
                                # print "RESET"

                    else:
                        self.suspicious_segments = []  # Reset
                        self.suspicious_segment_counter = 0  # Reset
                        passed_it = True  # Reset

                self.segments.remove(segment)
