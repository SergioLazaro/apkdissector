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
import os, threading
from core.threadAnalyzer import ThreadAnalyzer
from core.statistics import Statistics
from core.threadManager import ThreadManager
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
    print "main started!!"
    global dissector_global_dir
    config = ConfigurationReader()   #Config parameters
    #Check if the path is a file or a dir
    if os.path.isdir(path):
        #Checking if path is OK
        if path[-1:] is not "/":
            path = path + "/"
        apksnumber = len(os.listdir(path))      #Getting initial number of apks to analyze
        analyzeSample(path, config)
        #Could call to statistics.py to get some permissions statistics
        print "[*] Getting some statistics..."
        stats = Statistics(config.outputdir,apksnumber)
        stats.getStatistics()
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

def putUpTo5Tasks(tm, apks_list, samplepath , config):
    res = []
    for x in range(5):
        apk = apks_list.pop()
        apkpath = samplepath + apk
        t = ThreadAnalyzer(apkpath,config,"d")
        res.append(t)
    tm.add_task(res)


def analyzeSample(samplepath, config):
    start = time.time()
    #runningThreads = 1
    apks = os.listdir(samplepath)
    #tm = ThreadManager(config.threads)
    while True:
        if not apks: break
            #Generating apk path
            #apkpath = samplepath + apk
        tm  = ThreadManager(config.threads)
            #t = ThreadAnalyzer(apkpath,config,tm.lock,tm.working,"d")
        putUpTo5Tasks(tm,apks, samplepath, config)
        tm.wait_completition()
        print "num of apks: " + str(len(apks))
            #print "Launching new thread total: " + str(config.threads) + " running: " + str(runningThreads)
    '''
    waiting = threading.enumerate()
    for thread in waiting[1:]:
        thread.join()
    end = time.time()
    print "Total time spent (seconds): %.2f" % (end - start)
    '''

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
