
__author__='sergio'

from decimal import Decimal
import os, json

class PermissionCount:

    def __init__(self,permission,count):
        self.permission = permission
        self.count = count

class Statistics:

    def __init__(self, dir):
        self.dir = dir

    def getStatistics(self):
        apks = os.listdir(self.dir)
        results = list()
        i = 0
        for apk in apks:
            apkpath = self.dir+apk
            if os.path.isdir(apkpath):          #Working only on APK directories
                filepath = apkpath + "/" + apk + ".json"
                permissions = self.readPermissions(filepath)
                results = self.updateResult(results,permissions)
                i += 1
        for result in results:
            print "PERMISSION: " + result.permission + " VALUE: " + str(results.count)
        results = sorted(results, key=lambda x: x.count, reverse=True)
        print "============================================================"
        self.printStatistics(results,i)
        print "============================================================"
        print "[*] Analyzed apks: " + str(i)
        #print "[*] Total errors reported: " + str(self.apksnumber - (i))

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
        for val in results:
            percentage = (Decimal(val.count)/Decimal(i))*100
            print("PERMISSION: %s VALUE: %d PERCENTAGE: %.2f%%") % (val.permission,val.count, percentage)

        self.generateJSON(results,i)

    def generateJSON(self,results,i):
        fd = open(self.dir+"statistics.json","w")
        fd.write('{"permissions": [')
        for j,val in enumerate(results):
            percentage = (Decimal(val.count)/Decimal(i))
            if j < len(results) - 1:
                fd.write('{"permission":"' + val.permission + '","count":"' + str(val.count) +
                         '","percentage":"' + str(round(percentage,2)) + '"},')
            else:
                fd.write('{"permission":"' + val.permission + '","count":"' + str(val.count) +
                         '","percentage":"' + str(round(percentage,2)) + '"}')
        fd.write("]")
        #fd.write("],")
        #fd.write('"errors" :"' + str(self.apksnumber - (i)) + '"')
        fd.write("}")
        fd.close()

    def updateResult(self,results, permissions):
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