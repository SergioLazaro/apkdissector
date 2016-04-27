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
from statistics import Statistics
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
        #Checking if path is OK
        if path[-1:] is not "/":
            path = path + "/"
        apksnumber = os.listdir(path)
        analyzeSample(path, config)
        #Could call to statistics.py to get some permissions statistics
        print "[*] Getting some statistics..."
        stats = Statistics(config.outputdir)
        stats.getStatistics(apksnumber)
        print "[*] Errors are reported in " + config.errorlogdir
        print "[*] More output for each APK available in " + config.outputdir

    else:
        start = time.time()
        #analyzeAPK(path, config)
        apk = ThreadAnalyzer(path,config,"f")
        print "Analyzing APK " + path
        apk.run()
        #Wait until thread ends
        if apk.isAlive():
            apk.join()
        end = time.time()
        print "Total time spent (seconds): %.2f" % (end - start)

def analyzeSample(samplepath, config):
    start = time.time()
    runningThreads = 1
    apks = os.listdir(samplepath)
    threadList = list()
    for apk in apks:
        if int(runningThreads) <= int(config.threads):
            #Generating apk path
            apkpath = samplepath + apk

            t = ThreadAnalyzer(apkpath,config,"d")
            t.run()   #Starting new thread
            threadList.append(t)
            print "Launching new thread total: " + str(config.threads) + " running: " + str(runningThreads)
            runningThreads += 1
        else:
            print 'Waiting for threads...'
            #Wait until all threads are finished
            for thread in threadList:
                if thread.isAlive():        #A thread could have finished his job before join()...
                    thread.join()
            threadList = list() #Clear list that contains finished threads
            #Generating apk path
            apkpath = samplepath + apk

            t = ThreadAnalyzer(apkpath,config,"d")
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
