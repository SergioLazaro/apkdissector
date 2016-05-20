__author__ = 'sergio'

import sqlite3

from collector.pscoutDB import Permission
from permissionStack import StackElement
from permissionStack import PermissionStack


class DbMapper:

    def __init__(self,jsondbpath,pscoutdbpath,permission):
        self.jsondbpath = jsondbpath
        self.pscoutdbpath = pscoutdbpath
        self.permission = permission
        self.jsondb = None
        self.pscoutdb = None
        self._connect()
        self.showMapping()


    '''
        Method that maps the PScout DB with the JsonDB got after the json file parse.
        The match consist on a iteration over the PScout DB with a permission. When
        the list of PScout results is returned, the JsonDB check the same permission
        and returns the info stored about that permission.
        Now, we have two list of permission info from different sources. As the JsonDB
        row has a stack ,we have to check all the methods stored by each element of
        the stack.
        The map is done by checking the method name of a JsonDB row and a PScout row.
        If the method name matches, it prints all the info related to that match.
    '''
    def showMapping(self):

        pscoutlist = self.queryPScoutDB()       #List of PScout row object
        jsonlist = self.queryJsonDB()           #List of JsonDb row object
        i = 0
        for pscoutElem in pscoutlist:
            current_method = pscoutElem.callerMethod
            #Parsing the PscoutElem className (example: com/android/server/LocationManagerService)
            #Final result -> LocationManagerService
            current_class = pscoutElem.callerClass.split("/")
            current_class = current_class[len(current_class) - 1]
            for jsonElem in jsonlist:
                #Check all the stack...
                for stackElem in jsonElem.stack:
                    if stackElem.methodname == current_method and stackElem.classname == current_class:
                        i += 1
                        self.printMatch(stackElem,pscoutElem)
        print "[*] " + str(i) + " matches found."

    def printMatch(self,stackElem, pscoutElem):
        print "**"
        print "Stack-methodname: " + stackElem.methodname + " PSCOUT-methodname: " + pscoutElem.callerMethod
        print "Stack-classname: " + stackElem.classname + " PSCOUT-classname: " + pscoutElem.callerClass
        print "Stack-filename: " + stackElem.filename + " PSCOUT-filename: - "
        print "Sack-signature: - \t\t" + " PSCOUT-signature: " + pscoutElem.callerMethodDesc
        print "**"

    def queryJsonDB(self):
        if self.jsondb is not None:
            query = "SELECT hash,permission, methodname, uid, pid FROM permstacktable " \
                    "WHERE permission = '" + self.permission + "'"
            cursor = self.jsondb.execute(query)
            permissionList = list()
            i = 0
            for i,row in enumerate(cursor):
                #Now, we have to retrieve all the StackTrace from the stacktable table
                query2 = "SELECT filename, classname, methodname, count FROM stacktable " \
                         "WHERE hash = '" + row[0] + "'"
                stack_rows = self.jsondb.execute(query2)
                #Getting a list with all the StackTrace
                stack = list()
                for r in stack_rows:
                    stackElement = StackElement(r[0],r[1],r[2])
                    stack.append(stackElement)

                #PermissionStack(permission, uid, pid, methodname,stack)
                permissionStack = PermissionStack(row[1],row[3],row[4],row[2],stack)
                permissionList.append(permissionStack)
            print "[*] " + str(i) + " rows found with " + self.permission + " in JsonDB"
            return permissionList

    def queryPScoutDB(self):
        if self.pscoutdb is not None:
            query = "SELECT callerclass, callermethod, callermethoddesc FROM permissions " \
                    "WHERE permission = '" + self.permission + "'"
            cursor = self.pscoutdb.execute(query)
            permissionlist = list()
            for i, row in enumerate(cursor):
                elem = Permission(row[0],row[1],row[2])
                permissionlist.append(elem)

            print "[*] " + str(i) + " rows found with " + self.permission + " in PScoutDB"
            return permissionlist


    def _connect(self):
        self.jsondb = sqlite3.connect(self.jsondbpath)
        self.pscoutdb = sqlite3.connect(self.pscoutdbpath)
        if self.jsondb is None or self.pscoutdb is None:
            print "[!!] Cannot connect to databases. Exiting..."
            exit(-1)
