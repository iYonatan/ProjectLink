
from PythonServer import *

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1:])
    else:
        print "Usage: %s <clientPort> " % sys.argv[0]
