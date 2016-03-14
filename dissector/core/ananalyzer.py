__author__ = 'vaioco'


class AnAnalyzer:
    def __init__(self, t):
        self.target = t
        self.cls_list = []
        self.run()

    def get_cls_list(self):
        return self.cls_list

    def run(self):
        pass