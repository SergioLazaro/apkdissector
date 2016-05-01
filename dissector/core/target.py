import shutil

__author__ = 'vaioco'


from androguard.core import *
from androguard.core.bytecode import *
from androguard.core.bytecodes.dvm import *
from androguard.core.bytecodes.apk import *
from androguard.core.analysis.analysis import newVMAnalysis
from core.utils import *
from cPickle import dumps, loads
from exceptions import ZIPException
from androguard.decompiler.decompiler import *

'''
    APK 2target da analizzare
'''
class Target:
    def __init__(self, filename,config):
        self.cachedir = ''
        self.filename = filename
        self.config = config
        self.package_name = None
        self.open()
    def _print(self):
        return "Target info: \n\tpackage name: " + self.package_name.encode("utf-8") + \
               "\n\tfilename: " + self.filename

    def get_name(self):
        return self.filename

    def open(self):
        #aggiungere calcolo md5 dell apk e usarlo come nome per la sessione
        print 'opening : ' + self.filename
        try:
            self.apk = APK(self.filename)
            self.dvmf = DalvikVMFormat(self.apk.get_dex())
            self.vma = newVMAnalysis(self.dvmf)
            self.dvmf.set_vmanalysis(self.vma)
            self.package_name = self.apk.get_package()
            if self.package_name is None:
                print 'cannot retrive package name information for ' + self.filename
        except:
            print "cannot open the APK file"
            apkname = os.path.basename(os.path.splitext(self.filename)[0])
            errorlogpath = self.config.errorlogdir + apkname + ".txt"
            exception = ZIPException(errorlogpath,apkname)
            #shutil.rmtree(dir)

    def get_manifest(self):
        return self.apk.get_android_manifest_xml()

    def get_class(self, cname):
        return self.dvmf.get_class(cname)

    def get_classes(self):
        return self.dvmf.get_classes();

    def save_session(self, filename):
        print 'saving session in ' + filename
        l = [self.apk, self.dvmf, self.vma]
        self.cachedir = filename
        with open(filename, "w") as fd:
            fd.write(dumps(l,-1))

    def restore_session(self, filename):
        a,d,dx = loads(read(filename, binary=False))
        self.apk = a
        self.dvmf = d
        self.vma = dx
