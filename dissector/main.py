__author__ = 'vaioco && sergio'
import threading
from threading import Thread

import time

import sqlite3

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

python enforcementParser.py -i file1 -o /home/sid/android/malware/analysis
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
        start = time.time()
        analyzeSample(path, config)
        #Could call to statistics.py to get some permissions statistics
        end = time.time()
        print "Total time: %s" % (str(end-start))
        print "[*] Getting some statistics..."
        #stats = Statistics(config.outputdir)
        stats = Statistics(config.dbpath)
        stats.getStatisticsFromDB()
        print "[*] Errors are reported in " + config.errorlogdir
        print "[*] More output for each APK available in " + config.outputdir

    else:
        #apkname = os.path.basename(path)
        start = time.time()
        #analyzeAPK(path, config)
        apk = ThreadAnalyzer(path,config)
        print "Analyzing APK " + path
        apk.start()
        #Wait until thread ends
        #if apk.isAlive():
        #    apk.join()
        end = time.time()
        print "Total time spent (seconds): %.2f" % (end - start)

def putUpToNTasks(tm, apks_list, samplepath , config):
    res = []
    for x in range(int(config.threads)):
        if len(apks_list) > 0:
            apk = apks_list.pop()
            apkpath = samplepath + apk
            t = ThreadAnalyzer(apkpath,config)
            res.append(t)
    tm.add_task(res)


def analyzeSample(samplepath, config):
    apks = os.listdir(samplepath)
    while True:
        if not apks: break

        tm  = ThreadManager(config.threads)
        putUpToNTasks(tm,apks, samplepath, config)
        tm.wait_completition()

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
