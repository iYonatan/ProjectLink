from Communication import *
from Database import Connector

db_conn = Connector()
db_conn.connect()

comm = Communication(db_conn)
comm.run()
