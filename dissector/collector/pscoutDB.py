import sqlite3
import os

class PScoutDB:
    def __init__(self,api):
        self.api = api
        self.conn = None
        self.create()

    def create(self):
        self.dbname =  "dbs/" + str(self.api) + ".db"
        print 'creating dbname: ' + self.dbname
        self.conn = sqlite3.connect(self.dbname)
        print 'debugging conn: ' + str(self.conn)
        self.conn.execute(''' DROP TABLE IF EXISTS pscout''')
        query1 = '''
        CREATE TABLE pscout
               (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
               CALLERCLASS             VARCHAR,
               CALLERMETHOD            VARCHAR,
               CALLERMETHODDESC        VARCHAR,
               PERMISSION              VARCHAR,
               VERSION                 VARCHAR);
        '''
        self.conn.execute(query1)
        with open("PScout/" + str(self.api) + ".csv") as file:
            i = 1
            for line in file:
                list = line.split(",")
                print "Added record: %d\n" % (i)
                print "%s - %s - %s - %s - %s\n" % (list[0],list[1],list[2],list[3],list[4])
                self.conn.execute("INSERT INTO pscout (CALLERCLASS,CALLERMETHOD,CALLERMETHODDESC,PERMISSION,VERSION) "
                             "VALUES (?,?,?,?,?)",(list[0],list[1],list[2],list[3],list[4]));

            self.conn.commit()
            print "Records created successfully";

    def querypermission(self, permission):
        cursor = self.conn.execute("SELECT * from pscout WHERE PERMISSION = %s" % ("'" + permission + "'"))
        i = 0
        for row in cursor:
            i += 1
            print "ID = ", row[0]
            print "CALLERCLASS = ", row[1]
            print "CALLERMETHOD = ", row[2]
            print "CALLERMETHODDESC = ", row[3]
            print "PERMISSION = ", row[4]
            print "VERSION = ", row[5],"\n"

        if(i != 0):
            print "%d rows found" % (i)
        else:
            print "%s does not exists \n" % (permission)

        #Should return a list

    def close(self):
        self.conn.close()
