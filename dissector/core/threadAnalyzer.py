import shutil

__author__='sergio'

import threading, os, sys, traceback
from target import Target
from collector.manifest import Manifest
from analyzer.manifest import ManifestAnalyzer
from logger import Logger
from exceptions import ZIPException
from collector.hashesDB import hashesDB

#class ThreadAnalyzer (threading.Thread):
class ThreadAnalyzer ():
    #def __init__(self, apkpath, config,lock,working,type):
    def __init__(self, apkpath, config):
        #threading.Thread.__init__(self)
        self.apkpath = apkpath
        self.config = config
        #self.lock = lock
        #self.working = working

    #def run(self):
    def start(self):
        #Call to Analyze APK
        #Creating directory for the current apk

        apkname = os.path.basename(os.path.splitext(self.apkpath)[0])
        dir = self.config.outputdir + str(apkname) + "/"
        #Creating directory if not exists
        if not os.path.exists(dir):
            #print "Creating directory " + str(dir) + " for APK " + str(apkname) + "..."
            os.makedirs(dir)
            os.chmod(dir,0755)
        static_target = str(self.apkpath) #this must be the complete path of apk file
        logpath = self.config.outputdir + apkname + '/log.txt'
        log = Logger(logpath)

        #Opening APK with Androguard
        targetapp = Target(static_target,self.config)
        if targetapp.status:    #If open APK result is OK, we continue...
            if targetapp.package_name is not None:
                session_name = targetapp.package_name #usare md5, meglio
            else:
                session_name = "dummyname"

            #Check if the current APK has a cache file
            if os.path.isfile(dir + "cache"):
                log.write("Restoring session for " + apkname)
                targetapp.restore_session(dir + "cache")
            else:
                log.write("Saving session for " + apkname)
                targetapp.save_session(dir + "cache")

            # Creating database connection
            database = hashesDB(self.config.dbpath)
            database.connect()
            manifestInfo = Manifest(targetapp)

            #Changing stdout to apkName.txt file (Normal output and errors)
            manifestAnalysis = ManifestAnalyzer(manifestInfo,targetapp);
            log.write("analyzing...\n" + targetapp._print())
            #manifestInfo.checkPermissions(self.config,apkname,targetapp.package_name,log)          <- JSON
            manifestInfo.checkPermissionsInDB(self.config, apkname, database)                # <- DB
            log.write(apkname + " has been analyzed.")
            print apkname + " has been analyzed."
            print "**********************************************************"
            log.close()
            database.close()

        else:
            shutil.rmtree(dir)  #Deleting folder for apk analysis

        #deob = Deobfuscator(targetapp)
        #vmfilter = VirtualMethodsFilter(manifestAnalysis)
        #writer = HookWriter(manifestAnalysis,vmfilter)
        #writer.write(dest+'Fuffa.java')
        #print 'scritto'





