__author__ = 'sergio'

import os, sqlite3

class PermStackDb:

    def __init__(self,permissionStackElementList,dbpath,permission):
        self.permissionStackElementList = permissionStackElementList
        self.conn = None
        self.permission = permission
        if os.path.isdir(dbpath):    #DB file path or output path for DB
            if dbpath[-1:] is not "/":
                #Case -> create DB
                dbpath = dbpath + "/"

            self.dbpath = dbpath + "permission_stack.db"
            self.connect()
            self.createDB()
            if self.permission is not None:
                self.getPermissionInfo(self.permission)
        else:
            #Case -> DB exists
            self.dbpath = dbpath
            if os.path.isfile(self.dbpath):
                print "[*] DB path is correct. Checking permission..."
                self.connect()
                self.getPermissionInfo(permission)
            else:
                print "[!!] DB doesnt exist. Exiting..."
                exit(-1)

    def createDB(self):
        if self.conn is not None:
            print "[*] Creating db in " + self.dbpath
            self.conn.execute(''' DROP TABLE IF EXISTS permstacktable''')   #Check if table exists
            self.conn.execute(''' DROP TABLE IF EXISTS stacktable''')
            self.createPermissionStackTable()
            self.createStackTable()
            self.populateDB()
            print "[*] Database created successfuly in " + self.dbpath
        else:
            print "[!!] Problems while connecting with the DB"

    '''
        Method that iterates over the self.permissionStackElementList
        and insert the elements in the DB, if there is a connection
        to it.
    '''
    def populateDB(self):
        if self.conn is not None:
            count = 0
            for permissionStack in self.permissionStackElementList:
                count += self.insertIntoPermStackTable(permissionStack)

            self.conn.commit()  #Commit the changes
            print "[*] Total rows inserted: " + str(count)
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
            return 1
        else:
            print "[!] Hash " + permissionStackElem.hash + " already exists"
            return 0

    def insertIntoStackTable(self,hash,stack):
        print "[*] Adding " + str(len(stack)) + " elements to stacktable..."
        for i,stackElement in enumerate(stack):
            self.conn.execute("INSERT INTO stacktable (HASH,filename,classname,methodname,count) "
                                 "VALUES (?,?,?,?,?)",(hash,stackElement.filename, stackElement.classname,
                                                       stackElement.methodname,i));

    '''
        Method that checks if the [hash] passed as argument is currently inserted in the
        database. If the [hash] is inserted, the actual values are not inserted. [hash]
        is the concatenation of the unique fields, the stack object list and the permission.
    '''
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
        print "[*] Connecting to " + self.dbpath
        self.conn = sqlite3.connect(self.dbpath)

    def getPermissionInfo(self,permission):
        if self.conn is not None:
            print "[*] Checking " + permission
            query = "SELECT hash,permission, methodname, uid, pid FROM permstacktable " \
                    "WHERE permission = '" + permission + "'"
            cursor = self.conn.execute(query)
            i = 0
            for row in cursor:
                print "======================"
                print "         ROW " + str(i + 1)
                print "======================"
                print "Hash: " + row[0]
                print "Permission: " + row[1]
                print "Method name: " + row[2]
                print "UID: " + str(row[3])
                print "PID: " + str(row[4])

                #Now, we have to retrieve all the StackTrace from the stacktable table
                print "======================"
                print "      Stack Info      "
                print "======================"
                query2 = "SELECT filename, classname, methodname, count FROM stacktable " \
                         "WHERE hash = '" + row[0] + "'"
                stack_rows = self.conn.execute(query2)
                for r in stack_rows:
                    print "Element: " + str(r[3])
                    print "Filename: " + r[0]
                    print "Classname: " + r[1]
                    print "Methodname: " + r[2]
                i += 1
            if i == 0:
                print "[*] 0 matches found."
        else:
            print "[!!] Connection fail. Exiting..."

