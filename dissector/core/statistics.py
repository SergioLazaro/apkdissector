
__author__='sergio'

from decimal import Decimal
import os

class PermissionCount:

    def __init__(self,permission,count):
        self.permission = permission
        self.count = count

class Statistics:

    def __init__(self, dir, apksnumber):
        self.dir = dir
        self.apksnumber = apksnumber

    def getStatistics(self):
        apks = os.listdir(self.dir)
        results = list()
        i = 0
        for val in apks:
            apkpath = self.dir+val
            if os.path.isdir(apkpath):
                direlements = os.listdir(apkpath)   #'ls'
                permissions = self.getAnalyzedApks(direlements)  #Getting all apks directories
                results = self.updateResult(results,permissions)
                i += 1

        print "============================================================"
        self.printStatistics(results,i)
        print "============================================================"
        print "[*] Analyzed apks: " + str(i)
        print "[*] Total errors reported: " + str(self.apksnumber - (i))

    #Method used to exclude files and get only directories
    def getAnalyzedApks(self,direlements):
        permissions = list()
        for elem in direlements:
            if elem.endswith(".json"):
                permissions.append(elem)
        return permissions

    def printStatistics(self,results,i):
        for val in results:
            percentage = (Decimal(val.count)/Decimal(i))*100
            print("PERMISSION: %s VALUE: %d PERCENTAGE: %.2f%%") % (val.permission[:-5],val.count, percentage)

        response = raw_input("Do you want a JSON file?[Y/N]: ")
        if response is "Y" or response is "y":
            print "[*] JSON file created in " + self.dir
            self.generateJSON(results,i)

    def generateJSON(self,results,i):
        fd = open(self.dir+"statistics.json","w")
        fd.write('{"permissions": [')
        for j,val in enumerate(results):
            percentage = (Decimal(val.count)/Decimal(i))
            if j < len(results) - 1:
                fd.write('{"permission":"' + val.permission[:-5] + '","count":"' + str(val.count) +
                         '","percentage":"' + str(round(percentage,2)) + '"},')
            else:
                fd.write('{"permission":"' + val.permission[:-5] + '","count":"' + str(val.count) +
                         '","percentage":"' + str(round(percentage,2)) + '"}')
        fd.write("],")
        fd.write('"errors" :"' + str(self.apksnumber - (i)) + '"')
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