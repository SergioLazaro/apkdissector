import threading
from threading import Thread

import time

__author__ = 'vaioco && sergio'

from core.configurationreader import ConfigurationReader
from collector.manifest import Manifest
from core.target import Target
from analyzer.manifest import ManifestAnalyzer
from analyzer.deobfuscator import Deobfuscator
from core.filters import VirtualMethodsFilter
from core.writers import HookWriter
import sys
import optparse
import core.myglobals
import os
from core.threadAnalyzer import ThreadAnalyzer
#sys.path.insert(1, '/Users/vaioco/android_stuff/androguard')

static_target = 'apks/test-malware.apk'  #'/Users/vaioco/Lavoro/cert/youapp/base.apk'



#dest = '/Users/vaioco/ownCloud/documents/Dottorato/ProgettoPhd/apkdissector/'
#cache_dir = '/Users/vaioco/ownCloud/documents/Dottorato/ProgettoPhd/apkdissector/cache/'

#static_target = 'apks/'
dest = 'files/'
'''
/tmp/apks/....

python main.py -i file1 -o /home/sid/android/malware/analysis
'''
def main(path):
    global dissector_global_dir
    config = ConfigurationReader()   #Config parameters
    #Check if the path is a file or a dir
    if os.path.isdir(path):
        analyzeSample(path, config)
        #Could call to statistics.py to get some permissions statistics
        currentdir = os.getcwd()
        print "Getting some statistics..."
        os.system("python " + currentdir + "/statistics.py -d " + config.outputdir)
    else:
        start = time.time()
        #analyzeAPK(path, config)
        apk = ThreadAnalyzer(path,config)
        print "Analyzing APK " + path
        apk.run()
        #Wait until thread ends
        apk.join()
        end = time.time()
        print "Total time spent (seconds): %.2f" % (end - start)

'''
def analyzeAPK(apkpath, config):

    #Creating directory for the current apk
    apkname = os.path.basename(os.path.splitext(apkpath)[0])
    dir = config.outputdir + str(apkname) + "/"
    #Creating directory if not exists
    if not os.path.exists(dir):
        print "Creating directory " + str(dir) + " for APK " + str(apkname) + "..."
        os.makedirs(dir)
        os.chmod(dir,0755)

    static_target = str(apkpath) #this must be the complete path of apk file
    targetapp = Target(static_target)
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
'''

def analyzeSample(samplepath, config):
    #Check if samplepath is correct
    if samplepath[:-1] is not "/":
        samplepath = samplepath + "/"

    start = time.time()
    runningThreads = 0
    apks = os.listdir(samplepath)
    print "APKS: " + apks
    threadList = list()
    for apk in apks:
        print 'config.threads = ' + str(config.threads),
        print 'running: ' + str(runningThreads)
        if int(runningThreads) < int(config.threads):
            #Generating apk path
            apkpath = samplepath + apk

            #t = threading.Thread(target=analyzeAPK, args=(apkpath,config))
            t = ThreadAnalyzer(apkpath,config)
            t.run()   #Starting new thread
            threadList.append(t)
            runningThreads += 1
            print "Launching new thread total: " + str(config.threads) + " running: " + str(runningThreads)
            # break
        else:
            print 'Waiting for threads...'
            #Wait until all threads are finished
            for thread in threadList:
                if thread.isAlive():        #A thread could have finished his job before join()...
                    thread.join()
            threadList = list() #Clear list that contains finished threads
            #Launch thread of this iteration and append to our threadList
            #t = threading.Thread(target=analyzeAPK, args=(apkpath,config))
            #Generating apk path
            apkpath = samplepath + apk
            
            t = ThreadAnalyzer(apkpath,config)
            t.run()
            threadList.append(t)
            runningThreads = 1
            print "Launching new thread total: " + str(config.threads) + " running: " + str(runningThreads)

    print "Waiting to the last threads launched"
    for thread in threadList:
        if thread.isAlive():        #A thread could have finished his job before join()...
            thread.join()

    end = time.time()
    print "Total time spent (seconds): %.2f" % (end - start)


def print_help(parser):
    print "arguments error!!\n"
    parser.print_help()
    exit(-1)

if __name__ == "__main__":
    #PARAMETERS
    #-f, --file: APK file path
    #-d, --dir: Path to a directory with APKS
    core.myglobals.init()
    print core.myglobals.dissector_global_dir
    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', action="store", help="APK file path", dest="file",type="string")
    parser.add_option('-d','--dir', action="store", help="Path to a directory with APKs", dest="dir",type="string")

    (opts, args) = parser.parse_args()
    if opts.file is not None:
        main(opts.file)
    elif opts.dir is not None:
        main(opts.dir)
    else:
        print_help(parser)
