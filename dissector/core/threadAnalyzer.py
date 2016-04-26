__author__='sergio'

import threading, os, sys
from target import Target
from collector.manifest import Manifest
from analyzer.manifest import ManifestAnalyzer


class ThreadAnalyzer (threading.Thread):
    def __init__(self, apkpath, config):
        threading.Thread.__init__(self)
        self.apkpath = apkpath
        self.config = config

    def run(self):
        #Call to Analyze APK
        self.analyzeAPK(self.apkpath,self.config)

    def analyzeAPK(self,apkpath, config):

        #Creating directory for the current apk
        apkname = os.path.basename(os.path.splitext(apkpath)[0])
        dir = config.outputdir + str(apkname) + "/"
        #Creating directory if not exists
        if not os.path.exists(dir):
            print "Creating directory " + str(dir) + " for APK " + str(apkname) + "..."
            os.makedirs(dir)
            os.chmod(dir,0755)

        static_target = str(apkpath) #this must be the complete path of apk file
        try:
            targetapp = Target(static_target)
        except:
            print "Error appeared analyzing " + static_target
        if targetapp.package_name is not None:
            session_name = targetapp.package_name #usare md5, meglio
        else:
            session_name = "dummyname"
        #first we need to check if a cache file already exists
        #targetapp.save_session(core.myglobals.dissector_global_dir  + "/cache/" + session_name + '.andro')
        manifestInfo = Manifest(targetapp)

        #Changing stdout to apkName.txt file (Normal output and errors)
        print "Redirecting stdout to " + dir + "output.txt"
        fd = open(dir + 'output.txt','w')
        sys.stdout = fd
        manifestAnalysis = ManifestAnalyzer(manifestInfo,targetapp);
        print "Writing new JSON file with permissions..."
        #Should appear a new file called [files/permissions.json]
        print "Writing new JSON file with pscout mappings..."
        #Should appear a new file called []
        manifestInfo.checkPermissions(config,apkname)

        #Restoring stdout
        sys.stdout = sys.__stdout__
        fd.close()
        print apkname + " has been analyzed."
        print "**********************************************************"
        #deob = Deobfuscator(targetapp)
        #vmfilter = VirtualMethodsFilter(manifestAnalysis)
        #writer = HookWriter(manifestAnalysis,vmfilter)
        #writer.write(dest+'Fuffa.java')
        #print 'scritto'

