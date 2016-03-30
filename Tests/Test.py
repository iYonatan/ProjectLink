import bcrypt

password = b"hello"
hashed = bcrypt.hashpw(password, bcrypt.gensalt(10))
print hashed
if bcrypt.hashpw(password, "$2y$10$/p8.Z3iZP8rEdWSH1O/3.OMfi.yHJLu2g/kSRoPQZX7xCISYbnoaq") == hashed:
    print("It Matches!")

else:
    print "BYE"
