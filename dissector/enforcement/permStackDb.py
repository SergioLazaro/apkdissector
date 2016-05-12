__author__ = 'sergio'

import os, sqlite3

class PermStackDb:

    def __init__(self,permissionStackElementList,dbpath):
        self.permissionStackElementList = permissionStackElementList
        self.conn = None
        #Checking if path is OK
        if dbpath[-1:] is not "/":
            dbpath = dbpath + "/"
        self.dbpath = dbpath + "permission_stack.db"
        self.connect()
        self.createDB()

    def createDB(self):
        if self.conn is not None:
            self.conn.execute(''' DROP TABLE IF EXISTS permstacktable''')   #Check if table exists
            self.conn.execute(''' DROP TABLE IF EXISTS stacktable''')
            self.createPermissionStackTable()
            self.createStackTable()
            self.populateDB()
        else:
            print "[!!] Problems while connecting with the DB"

    def populateDB(self):
        if self.conn is not None:
            for permissionStack in self.permissionStackElementList:
                self.insertIntoPermStackTable(permissionStack)

            self.conn.commit()  #Commit the changes
        else:
            print "[!!] Problems while connecting with the DB"

    def insertIntoPermStackTable(self,permissionStackElem):
        insert = self.isHashFound(permissionStackElem.hash)
        if insert:
            print "[*] Adding new element to permstacktable..."
            self.conn.execute("INSERT INTO permstacktable (HASH,PERMISSION,METHODNAME,UID,PID) "
                                 "VALUES (?,?,?,?,?)",(permissionStackElem.hash,permissionStackElem.permission,
                                    permissionStackElem.methodname,permissionStackElem.uid,permissionStackElem.pid));
            self.insertIntoStackTable(permissionStackElem.hash,permissionStackElem.stack)
        else:
            print "[!] Hash " + permissionStackElem.hash + " already exists"

    def insertIntoStackTable(self,hash,stack):
        print "[*] Adding " + str(len(stack)) + " elements to stacktable..."
        for i,stackElement in enumerate(stack):
            self.conn.execute("INSERT INTO stacktable (HASH,filename,classname,methodname,count) "
                                 "VALUES (?,?,?,?,?)",(hash,stackElement.filename, stackElement.classname,
                                                       stackElement.methodname,i));

    def isHashFound(self,hash):
        if self.conn is not None:
            query = "SELECT COUNT(*) FROM permstacktable WHERE HASH = '" + hash + "'"
            rows_count = self.conn.execute(query)
            if rows_count.fetchone()[0] == 0:   #Not inserted yet
                return True
            else:   #Is already inserted
                return False
        else:
            print "[!!] Database connection lost"
            exit(-1)

    '''
        Method used to generate the permstacktable which contains information about
        the elements.
    '''
    def createPermissionStackTable(self):
        query1 = '''
        CREATE TABLE permstacktable
           (HASH VARCHAR PRIMARY KEY ,
           PERMISSION VARCHAR,
           METHODNAME VARCHAR,
           UID NUMBER ,
           PID NUMBER);
        '''
        self.conn.execute(query1)

    '''
        Method used to generate the stacktable which contains information about
        stack elements.
    '''
    def createStackTable(self):
        query2 = '''
        CREATE TABLE stacktable
               (HASH VARCHAR REFERENCES permstacktable,
               filename VARCHAR,
               classname VARCHAR,
               methodname VARCHAR,
               count NUMBER);
        '''
        self.conn.execute(query2)

    '''
        Connect to the database inserted in the path [dbpath]. If there is not a database created,
        this method creates it.
    '''
    def connect(self):
        self.conn = sqlite3.connect(self.dbpath)

