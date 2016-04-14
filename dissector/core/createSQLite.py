__author__ = 'sergio'
import sqlite3

conn = sqlite3.connect('../dbs/example.db')
conn.execute(''' DROP TABLE IF EXISTS api22''')
query1 = '''
CREATE TABLE %s
       (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
       CALLERCLASS             VARCHAR,
       CALLERMETHOD            VARCHAR,
       CALLERMETHODDESC        VARCHAR,
       PERMISSION              VARCHAR,
       VERSION                 VARCHAR);
''' % ("api22")
conn.execute(query1)

with open("../PScout/5.1.1.csv") as file:
    i = 1
    for line in file:
        list = line.split(",")
        print "Added record: %d\n" % (i)
        print "%s - %s - %s - %s - %s\n" % (list[0],list[1],list[2],list[3],list[4])
        conn.execute("INSERT INTO api22 (CALLERCLASS,CALLERMETHOD,CALLERMETHODDESC,PERMISSION,VERSION) "
                     "VALUES (?,?,?,?,?)",(list[0],list[1],list[2],list[3],list[4]));

    conn.commit()
    print "Records created successfully";
conn.close()