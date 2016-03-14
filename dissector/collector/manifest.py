__author__ = 'vaioco'

from core.acollector import Acollector
from collections import defaultdict

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
                    print 'AAAAAA sto analizzando item: ' + item.getAttribute('android:name')
                else:
                    pass