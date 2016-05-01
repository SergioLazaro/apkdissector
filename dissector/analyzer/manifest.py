__author__ = 'vaioco'

from core.ananalyzer import AnAnalyzer

class ManifestAnalyzer(AnAnalyzer):
    def __init__(self, c, t):
        self.collector = c
        self.target = t
        AnAnalyzer.__init__(self,self.target)

    def run(self):
        self.analyze_all()

    def analyze_all(self):
        target_dict = self.collector.get_data()
        self._analyze(target_dict)

    def _analyze(self, target_dict):
        tags = self.collector.get_target_tags()
        for t in tags:
            #print 'tag : ' + t
            for elem in target_dict[t]:
                #print 'analyzer manifest, elem: ' + elem.get_name()
                c = self.target.get_class('L' + elem.get_name().replace('.','/') + ';')
                if c is None:
                    continue
                self.cls_list.append(c)
                for method in  c.get_methods():
                    if method.get_access_flags_string() == "public":
                        pass

