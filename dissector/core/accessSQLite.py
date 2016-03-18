import sqlite3

conn = sqlite3.connect('../dbs/api22.db')
cursor = conn.execute("SELECT * from api22 WHERE PERMISSION = 'android.permission.INTERNET'")
i = 0
for row in cursor:
    i += 1
    print "ID = ", row[0]
    print "CALLERCLASS = ", row[1]
    print "CALLERMETHOD = ", row[2]
    print "CALLERMETHODDESC = ", row[3]
    print "PERMISSION = ", row[4]
    print "VERSION = ", row[5],"\n"

print "METHODS: %d" % (i)
