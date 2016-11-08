
__author__='sergio'

from collector.hashesDB import hashesDB
from decimal import Decimal
import os, json


class PermissionCount:

    def __init__(self,permission,count):
        self.permission = permission
        self.count = count

class Statistics:

    def __init__(self, path):
        self.path = path
        self.errors = 0
        self.apks = list()
        if os.path.isdir(self.path):
            self.checkErrors()

    def getStatisticsFromDB(self):
        database = hashesDB(self.path)
        database.connect()

        hashes = database.create_cursor("SELECT DISTINCT hash FROM analyzed")
        results = list()
        i = 0
        for apk_hash in hashes:
            hash = apk_hash[0]
            permissions = self.getPermissionsFromTuples(database, hash)
            results = self.updateResult(results, permissions)
            i += 1

        self.printStatistics(results,i)

    '''
        * Database = hashesDB database connected
        * hash = apk hash

        Method needed to get a permission list related to an apk hash.
        [permissions] will contain a list with permissions.
    '''
    def getPermissionsFromTuples(self, database, hash):

        permissions_tuple = database.create_cursor("SELECT permission FROM analyzed WHERE hash = '%s'" % hash)
        permissions = list()

        for permission in permissions_tuple:
            permissions.append(permission[0])

        return permissions

    def checkErrors(self):
        apks = os.listdir(self.path)
        for apk in apks:
            apkpath = self.path + apk + "/"
            #Checking that we have a empty directory
            if os.path.isdir(apkpath):
                if os.listdir(apkpath) == []:
                    self.errors += 1
                    os.removedirs(apkpath)  #Delete empty APK folder
                else:
                    self.apks.append(apk)

    def getStatisticsFromFiles(self):
        results = list()
        i = 0
        for apk in self.apks:
            filepath = self.path + apk + "/" + apk + ".json"
            permissions = self.readPermissions(filepath)
            results = self.updateResult(results,permissions)
            i += 1


        self.printStatistics(results,i)


    '''
        Method used to read the permissions used by an analyzed APK
    '''
    def readPermissions(self,filepath):
        permissions = list()
        with open(filepath) as data_file:
            data = json.load(data_file)
            for permission in data['mapping']:
                permissions.append(permission['permission'])
        return permissions

    def printStatistics(self,results,i):
        results = sorted(results, key=lambda x: x.count, reverse=True)
        print "============================================================"
        for val in results:
            percentage = (Decimal(val.count)/Decimal(i))*100
            print("PERMISSION: %s VALUE: %d PERCENTAGE: %.2f%%") % (val.permission,val.count, percentage)
        print "============================================================"
        print "[*] Analyzed apks: " + str(i)
        print "[*] Total errors reported: " + str(self.errors)

        self.generateJSON(results,i)

    def generateJSON(self,results,i):
        fd = open(self.path+"statistics.json","w")
        fd.write('{"permissions": [')
        for j,val in enumerate(results):
            percentage = (Decimal(val.count)/Decimal(i))
            if j < len(results) - 1:
                fd.write('{"permission":"' + val.permission + '","count":"' + str(val.count) +
                         '","percentage":"' + str(round(percentage,2)) + '"},')
            else:
                fd.write('{"permission":"' + val.permission + '","count":"' + str(val.count) +
                         '","percentage":"' + str(round(percentage,2)) + '"}')
        fd.write("],")
        fd.write('"errors" :"' + str(self.errors) + '"')
        fd.write("}")
        fd.close()

    def updateResult(self,results, permissions):
        #Delete repeated elements in permissions
        permissions = sorted(set(permissions))
        for tmppermission in permissions:
            position = -1
            for i,existingpermission in enumerate(results):
                if existingpermission.permission == tmppermission:
                    position = i

            if position == -1:  #tmppermission does not exists
                #Create new PermissionCount
                p = PermissionCount(tmppermission,1)
                #Append new PermissionCount
                results.append(p)
            else:           #tmppermission exists so we have to increment the value
                p = results[position]
                p.count += 1
        return results