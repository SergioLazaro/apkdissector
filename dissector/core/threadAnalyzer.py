import shutil

__author__='sergio'

import threading, os, sys, traceback
from target import Target
from collector.manifest import Manifest
from analyzer.manifest import ManifestAnalyzer

#class ThreadAnalyzer (threading.Thread):
class ThreadAnalyzer ():
    #def __init__(self, apkpath, config,lock,working,type):
    def __init__(self, apkpath, config,_type):
        #threading.Thread.__init__(self)
        self.apkpath = apkpath
        self.config = config
        self.type = _type
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
        #Catching Androguard exception
        try:
            targetapp = Target(static_target)
            if targetapp.package_name is not None:
                session_name = targetapp.package_name #usare md5, meglio
            else:
                session_name = "dummyname"

            cache_exists = self.checkCacheDir(apkname)
            if cache_exists:
                print "Restoring session for " + apkname
                targetapp.restore_session(self.config.cachedir + apkname + ".json")
            else:
                print "Saving session for " + apkname
                targetapp.save_session(self.config.cachedir + apkname + ".json")
            exit(0)
            manifestInfo = Manifest(targetapp)
            #first we need to check if a cache file already exists
            #targetapp.save_session(core.myglobals.dissector_global_dir  + "/cache/" + session_name + '.andro')

            #Changing stdout to apkName.txt file (Normal output and errors)
            #print "Redirecting stdout to " + dir + "output.txt"
            fd = open(dir + 'output.txt','w')
            sys.stdout = fd
            manifestAnalysis = ManifestAnalyzer(manifestInfo,targetapp);
            print "analyzing: "
            targetapp._print()
            manifestInfo.checkPermissions(self.config,apkname)
            #Restoring stdout
            sys.stdout = sys.__stdout__
            fd.close()
            print apkname + " has been analyzed."
            print "**********************************************************"
        except:
            if type is "d":
                print "[!!] Error appeared analyzing " + static_target
                fd = open(self.config.errorlogdir + apkname + ".txt","w")
                err = traceback.format_exc()
                fd.write(apkname + "\n" + str(err))
                fd.close
                shutil.rmtree(dir)
            else:
                raise
        '''
        if self.lock.locked():
            print "Thread " + str(self.id) + " RELEASE"
            try:
                self.lock.release()
            except:
                print "Lock unlocked."
            self.working -= 1
        '''
        #deob = Deobfuscator(targetapp)
        #vmfilter = VirtualMethodsFilter(manifestAnalysis)
        #writer = HookWriter(manifestAnalysis,vmfilter)
        #writer.write(dest+'Fuffa.java')
        #print 'scritto'

    def checkCacheDir(self, apkname):
        caches = os.listdir(self.config.cachedir)
        found = False
        i = 0
        while not found and i < len(caches):
            print "CACHE FILE: " + caches[i][-5] + " - APKNAME: " + apkname
            if caches[i][-5] == apkname:
                found = True
            i += 1
        return found



