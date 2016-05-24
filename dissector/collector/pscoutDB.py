__author__ = 'sergio'

import sqlite3
import os
import core

class PScoutDB:
    def __init__(self,api,dbpath):
        self.api = api
        self.destinationpath = core.myglobals.dissector_global_dir
        self.conn = None
        self.dbpath = dbpath + str(api) + ".db"
        if not os.path.exists(self.dbpath):
            #print 'creating the dbpath: ' + self.dbpath
            self.create()

    #The DB should be populated if we want to use it
    def connect(self):
        #print 'connecting to : ' + str(self.dbpath)
        self.conn = sqlite3.connect(self.dbpath)

    def create(self):
        self.connect()  #Connect to the DB
        self.conn.execute(''' DROP TABLE IF EXISTS pscout''')   #Check if table exists
        query1 = '''
        CREATE TABLE pscout
               (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
               CALLERCLASS             VARCHAR,
               CALLERMETHOD            VARCHAR,
               CALLERMETHODDESC        VARCHAR,
               PERMISSION              VARCHAR,
               VERSION                 VARCHAR);
        '''
        self.conn.execute(query1)   #Creating the table always
        #Read all rows of the file and insert it in new DB created
        with open(self.destinationpath + "/pscout_files/" + str(self.api) + ".csv") as file:
            i = 1
            for line in file:
                list = line.split(",")
                self.conn.execute("INSERT INTO pscout (CALLERCLASS,CALLERMETHOD,CALLERMETHODDESC,PERMISSION,VERSION) "
                             "VALUES (?,?,?,?,?)",(list[0],list[1],list[2],list[3],list[4]));

            self.conn.commit()  #Commit the changes
            #print "Records created successfully";

    #Query all rows looking for <permission>
    def querypermission(self, permission):

        cursor = self.conn.execute("SELECT callerClass, callerMethod, callerMethodDesc, permission "
                                   "from pscout WHERE PERMISSION = %s" % ("'" + permission + "'"))
        array = list()
        #print "Checking permissions of " + str(permission) + "..."
        for row in cursor:
            p = Permission(row[0],row[1],row[2], row[3])
            array.append(p)
        if(len(array) != 0):
            pass
            #print "%d rows found" % (len(array))
        else:
            pass
            #TODO: catch errors
            #print "%s does not exists \n" % (permission)

        return array

    #Close DB connection
    def close(self):
        self.conn.close()

class Permission:

    def __init__(self,callerClass,callerMethod, callerMethodDesc, permission):
        self.callerClass = callerClass
        self.callerMethod = callerMethod
        self.callerMethodDesc = callerMethodDesc
        self.permission = permission

