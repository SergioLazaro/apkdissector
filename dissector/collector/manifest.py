__author__ = 'vaioco'

from dissector.core.acollector import Acollector
from collections import defaultdict
from dissector.core.writers import JsonWrite
from dissector.collector.pscoutDB import PScoutDB
from dissector.collector.pscoutDB import Permission

import json

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
        print self.target.get_manifest().toprettyxml()
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
                    #print 'AAAAAA sto analizzando item: ' + item.getAttribute('android:name')
                    #Adding new <uses-permission> entry
                    writer.add(item.getAttribute('android:name'))
                else:
                    pass
        #Writing all items added before in our file
        #Maybe, we could add the name of the analyzed apk
        #example: whatsapp_permissions.txt/json/...
        writer.write("../files/permissions.json")

    def checkPermissions(self,version):
        with open("../files/permissions.json","r") as file:
            data = json.load(file)  #Our JSON file

        db = PScoutDB(version)
        for permission in data["permissions"]:
            db.connect()                                            #Connecting to the DB
            array = db.querypermission(permission["permission"])    #Getting info for permission['permission']
                                                                    #in the DB called <version.db>
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #!!  Create new dir with apk name !!!
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            dir = "blabla/"

            #Create new JSON file [path = apkName_permission.json]
            path = str(dir) + str(permission["permission"]) + ".json"
            file = open(path,"w")
            file.write("{'pscout':[")
            #Iterate over the array of Permission objects
            i = 0
            for p in array:
                file.write("{'callerClass':'" + p.self.callerClass + "',")
                file.write("{'callerMethod':'" + p.self.callerMethod + "',")
                file.write("{'callerMethodDesc':'" + p.self.callerMethodDesc + "'}")
                if(i < (len(array) - 1)):
                    file.write(",")
                    i += 1

            file.write("]}")