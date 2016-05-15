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

    def showMapping(self):

        pscoutlist = self.queryPScoutDB()
        jsonlist = self.queryJsonDB()

        for pscoutElem in pscoutlist:
            method = pscoutElem.callerMethod
            for jsonElem in jsonlist:
                for stackElem in jsonElem.stack:
                    print stackElem.methodname +  " - " + method
                    if stackElem.methodname == method:
                        print "MATCH"
                        self.printMatch(stackElem,pscoutElem)

    def printMatch(self,stackElem, pscoutElem):
        print "Stack-methodname: " + stackElem.methodname + " PSCOUT-methodname: " + pscoutElem.callerMethod
        print "Stack-classname: " + stackElem.classname + " PSCOUT-classname: " + pscoutElem.callerClass
        print "Stack-filename: " + stackElem.filename + " PSCOUT-filename: " + pscoutElem.callerMethodDesc

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
