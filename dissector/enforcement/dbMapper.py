import hashlib

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
        self.notMatches = list()
        self.showMapping()
        self.checkNotMatches()

    def checkNotMatches(self):
        if len(self.notMatches) > 0:
            print "[*] Looking for " + str(len(self.notMatches)) + " possible matches..."
            printedlist = list()
            for jsonElem in self.notMatches:
                for stackElem in jsonElem.stack:
                    possibleMatches = self.queryPScoutDB(stackElem)
                    for pscoutElem in possibleMatches:
                        if pscoutElem.callerMethod == stackElem.methodname:
                            info = InfoToShow(stackElem.methodname, stackElem.classname, stackElem.filename,
                                              pscoutElem.callerMethodDesc, pscoutElem.permission)
                            shouldPrint = self.isPrinted(info.hash, printedlist)    #Check if is printed or not...
                            if shouldPrint:
                                #Print the element and append it to the currently printed objects
                                self.printMatch(info)
                                printedlist.append(info)

        else:
            print "[*] No possible matches found."

    def isPrinted(self,hash, printedlist):
        shouldPrint = True
        for elem in printedlist:
            if elem.hash == hash:
                shouldPrint = False

        return shouldPrint

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
        self._connect()
        pscoutlist = self.queryPScoutDB(None)       #List of PScout row object
        jsonlist = self.queryJsonDB()           #List of JsonDb row object
        i = 0
        if len(pscoutlist) > 0 and len(jsonlist) > 0:
            for jsonElem in jsonlist:
                found = False
                for pscoutElem in pscoutlist:
                    #Check all the stack...
                    for stackElem in jsonElem.stack:
                        if stackElem.methodname == pscoutElem.callerMethod and stackElem.classname == pscoutElem.callerClass:
                            i += 1
                            info = InfoToShow(stackElem.methodname, stackElem.classname, stackElem.filename,
                                              pscoutElem.callerMethodDesc, pscoutElem.permission)
                            self.printMatch(info)   #Print match info
                            found = True
                if not found:
                    self.notMatches.append(jsonElem)

            print "[*] PScout elements: " + str(len(pscoutlist))
            print "[*] PermStack elements: " + str(len(jsonlist))
            print "[*] " + str(i) + " matches found."
        elif len(pscoutlist) == 0 and len(jsonlist) > 0:
            #Check all the jsonElements in the PScout database using the classname
            self.notMatches = jsonlist
        else:
            print "[*] No matches found for permission " + self.permission


    def printMatch(self,infoObject):
        print "**"
        print "Methodname: " + infoObject.methodname
        print "Classname: " + infoObject.classname
        print "Filename: " + infoObject.filename
        print "Signature: " + infoObject.signature
        print "Permission: " + infoObject.permission
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

    def queryPScoutDB(self,stackElem):
        if self.pscoutdb is not None:
            permissionlist = list()
            if stackElem is not None:   #Query using the classname as identifier
                query = "SELECT callerclass, callermethod, callermethoddesc, permission FROM permissions " \
                    "WHERE callerClass = '" + stackElem.classname + "'"
                cursor = self.pscoutdb.execute(query)
                for row in cursor:
                    elem = Permission(row[0],row[1],row[2],row[3])
                    permissionlist.append(elem)
            else:           #Query using the permission as identifier
                query = "SELECT callerclass, callermethod, callermethoddesc, permission FROM permissions " \
                        "WHERE permission = '" + self.permission + "'"
                cursor = self.pscoutdb.execute(query)
                i = 0
                for row in cursor:
                    elem = Permission(row[0],row[1],row[2],row[3])
                    permissionlist.append(elem)
                    i += 1
                print "[*] " + str(i) + " rows found with " + self.permission + " in PScoutDB"
            return permissionlist

    def _connect(self):
        self.jsondb = sqlite3.connect(self.jsondbpath)
        self.pscoutdb = sqlite3.connect(self.pscoutdbpath)
        if self.jsondb is None or self.pscoutdb is None:
            print "[!!] Cannot connect to databases. Exiting..."
            exit(-1)

class InfoToShow:

    def __init__(self, methodname, classname, filename, signature, permission):
        self.methodname = methodname
        self.classname = classname
        self.filename = filename
        self.signature = signature
        self.permission = permission
        self.hash = self.generateHash()

    def generateHash(self):
        concatenation = self.methodname + "," + self.classname + "," + self.filename + "," +\
                        self.signature + "," + self.permission
        return hashlib.sha1(concatenation).hexdigest()
