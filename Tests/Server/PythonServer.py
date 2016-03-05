# region ----------   ABOUT   -----------------------------
"""
##################################################################
# Created By:  Michael Chernovilski                              #
# Date: 20/09/2014                                               #
# Name: Server  between GUI and clients                          #
# Version: 1.0                                                   #
# Windows Tested Versions: Win 7 32-bit                          #
# Python Tested Versions: 2.6 32-bit                             #
# Python Environment  : PyCharm                                  #
##################################################################
"""
# endregion

# region ----------   IMPORTS   -----------------------------
import os
import socket
import sys
import threading

# endregion


# region -----  CONSTANTS  -----
# For every client to been thread
THREAD_LIMIT = 50
GUI_PORT = 9669
SERVER_ABORT = "Aborting the server..."


# endregion

# region ----------   CLASSES   -----------------------------
# region -----  PythonServer CLASS  -----
class PythonServer(threading.Thread):
    # -----  DATA  -----
    listenerSock = None
    # Dictionary for client connctions : Key - ip  Value - SessionWithClient
    open_clients = {}

    # constructor 
    def __init__(self, gui, listenerPort):
        self.gui = gui
        self.listenerPort = listenerPort
        threading.Thread.__init__(self)

    # the main thread function
    def run(self):
        import SessionWithClient
        self.gui.guiSock.send("Server running...Waiting for a connection...#")  # to GUI
        try:
            # Listener socket
            listenerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listenerSock.bind(("", self.listenerPort))
            listenerSock.listen(5)
            self.gui.guiSock.send("Listening to clients...#")  # to GUI

            while True:
                clientSock, addr = listenerSock.accept()
                # Thread creating loop
                while True:
                    if threading.activeCount() < THREAD_LIMIT:
                        clientIP = addr[0]  # key - IP client
                        # Check if client connected in pass
                        if clientIP in self.open_clients:
                            # Callback Connection by IP clientIP
                            self.gui.guiSock.send("Callback Connection by " + clientIP + " clientIP#")  # to GUI
                        else:
                            # First Connection by IP  clientIP
                            sessionWithClient = SessionWithClient(self, clientSock, addr)
                            sessionWithClient.start()
                        break
        except socket.error, er_msg:
            error_code = er_msg[0]
            if error_code == 10048:
                self.gui.guiSock.send("Port " + str(self.listenerPort) + " is busy#")  # to GUI
            else:
                self.gui.guiSock.send(str(er_msg) + "#")  # to GUI
        except Exception as er_msg:
            self.gui.guiSock.send(str(er_msg) + "#")  # to GUI


# endregion

# region -----  CLASS  GUI  -----
class Gui(threading.Thread):
    pythonServer = None

    # constructor
    def __init__(self):
        # socket between the this server and the GUI
        self.guiSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.guiSock.connect(("127.0.0.1", GUI_PORT))
        threading.Thread.__init__(self)

    # the main function
    def run(self):
        while True:
            # Wait message from GUI 
            data = self.guiSock.recv(1024)
            if len(data) > 0:
                pass


# endregion
# endregion


# region ----------   MAIN   -----------------------------

def main(args):
    """
    Description: Main function, connect to target server, establish protocol,

    Input:
         args - list of command line arguments
                1) - listener port
                :param args:
    """
    try:
        gui = Gui()  # connection to GUI process
        gui.start()  # start thtread loop for session with GUI
        try:
            from SessionWithClient import *
            # construct server for sessions with clients     
            #                                    listenerPort  
            gui.pythonServer = PythonServer(gui, int(args[0]))
            gui.pythonServer.start()
        except ImportError:
            gui.guiSock.send("pyCrypto module is not installed. " + SERVER_ABORT + "#")  # to GUI
            sys.exit("# pyCrypto module is not installed. " + SERVER_ABORT)
    except socket.error, e:
        print e

# endregion
