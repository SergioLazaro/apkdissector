__author__ = 'vaioco && sergio'

from collections import defaultdict
from core.writers import JsonWrite
from collector.pscoutDB import PScoutDB
from core.acollector import Acollector

import json
import os, sys

class Receiver:
    def __init__(self, name, exported, xml):
        self.name = name
        self.exported = exported
        self.xmlelement = xml

    def get_name(self):
        return self.name

    def to_string(self):
        return self.xmlelement.toxml()

class Activity:
    def __init__(self, name, exported, xml):
        self.name = name
        self.exported = exported
        self.xmlelement = xml

    def get_name(self):
        return self.name

    def to_string(self):
        return self.xmlelement.toxml()

class Service:
    def __init__(self, name, exported, xml):
        self.name = name
        self.exported = exported
        self.xmlelement = xml

    def get_name(self):
        return self.name

    def to_string(self):
        return self.xmlelement.toxml()

class Permission:
    def __init__(self,name):
        self.name = name

    def get_name(self):
        return self.name

class Manifest(Acollector):
    def __init__(self,target):
        self.collected_data = defaultdict(list)
        #self.target_tags = ['service', 'activity', 'receiver']
        self.target_tags = ['uses-permission']
        Acollector.__init__(self,target)

    def get_target_tags(self):
        return self.target_tags

    def get_data(self):
        return self.collected_data

    def run(self):
        print 'analyzing manifest ... '
        self.analyze_manifest()

    def analyze_manifest(self):
        #print self.target.get_manifest().toprettyxml()
        self.xmlmanifest = self.target.get_manifest()
        #print self.xmlmanifest
        self.collect_all()

    def collect_all(self):
        writer = JsonWrite()    #Creating our JsonWrite class
        for tag in self.target_tags:
            tag_list = self.xmlmanifest.getElementsByTagName(tag)
            for item in tag_list:
                #print 'porcodio: ' + tag
                #print 'check = ' + str(tag.rstrip() == "uses-permission")
                name = item.getAttribute('android:name')
                exp = item.getAttribute('android:exported')
                if tag == 'service':
                    self.collected_data[tag].append(Service(name,exp,item))
                elif tag == 'activity':
                    self.collected_data[tag].append(Activity(name,exp,item))
                elif tag == 'receiver':
                    self.collected_data[tag].append(Receiver(name,exp,item))
                elif tag == 'uses-permission':
                    #Adding new <uses-permission> entry
                    self.collected_data[tag].append(Permission(name))
                    #writer.add(item.getAttribute('android:name'))
                else:
                    pass
        #Writing all items added before in our file
        #Maybe, we could add the name of the analyzed apk
        #example: whatsapp_permissions.txt/json/...
        #print "=============================="
        #print "Total permissions used: " + str(len(self.collected_data['uses-permission']))
        #print "=============================="
        #writer.write("files/permissions.json")

    def checkPermissions(self,config,apkname,package_name,log):

        dir = config.outputdir + str(apkname) + "/"
        db = PScoutDB(config.version,config.dbpath)
        #Create new JSON file for permission_name.json
        path = dir + apkname + ".json"
        #Reporting APK info in log file
        log.write("Opening JSON file in " + path)
        log.write("Writing JSON file with PScout permissions mapping...")
        log.write("hash: " + apkname)
        log.write("package_name: " + package_name)
        log.write("manifest_permissions:")
        file = open(path,"w")   #Opening JSON with PScout mapping information
        #Populating JSON file
        file.write('{"hash":"' + apkname + '",\n')
        file.write('"package_name":"' + package_name + '",\n')
        file.write('"mapping":[\n')
        for j, permission in enumerate(self.collected_data['uses-permission']):   #Getting all entries for a permission
            current = permission.get_name()     #Current permission
            log.write("\t" + current)
            file.write('\t{"permission":"' + current + '",\n')
            file.write('\t"info":[')
            db.connect()                            #Connecting to the DB

            #Getting info for permission['permission'] in the DB called <version.db>
            array = db.querypermission(current)
            if len(array) > 0:
                file.write('\n')
                #Iterate over the array of Permission objects
                i = 0
                for p in array:
                    file.write('\t\t{"callerClass":"' + p.callerClass + '",')
                    file.write('"callerMethod":"' + p.callerMethod + '",')
                    if(i < (len(array) - 1)):
                        file.write('"callerMethodDesc":"' + p.callerMethodDesc + '"},\n')
                    else:
                        file.write('"callerMethodDesc":"' + p.callerMethodDesc + '"}\n')
                    i += 1
            #Check if we have more to write
            if j < (len(self.collected_data['uses-permission']) - 1):
                file.write("]},\n")

            j += 1
        file.write("]}]}")
        log.write("JSON file with PScout permissions mapping written successfuly")
        file.close()
