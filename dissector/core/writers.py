__author__ = 'vaioco'

from core.ananalyzer import AnAnalyzer
from core.filters import  VirtualMethodsFilter
from jinja2 import Environment, PackageLoader
from core.filters import TargetVirtualMethod
import json

class ConfigEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o,TargetVirtualMethod):
            return o.name
        return json.JSONEncoder.default(self,o)

class HookWriter:
    def __init__(self, analyzer, filter):
        self.analyzer = analyzer
        self.filter = filter
        self.filter.filtering()
        self.env = Environment(loader=PackageLoader('core', 'templates'))
        self.template = self.env.get_template('target_virtual_methods.java')

    def write(self, filename):
        f = open(filename, 'w')
        c = self.filter.get_data()
        s = self.template.render(_dict=c)
        f.write("%s\n" % s.encode('utf-8'))
        f.close()
        print 'json:'
        print json.dumps(c, cls=ConfigEncoder)

class DeobfuscatorWriter:
    @staticmethod
    def write(filename,s):
        with open(filename, "a") as fd:
            fd.write("%s\n" % s)
            fd.close()