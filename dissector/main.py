import threading
from threading import Thread

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
    else:
        analyzeAPK(path, config)

def analyzeAPK(apkpath, config):
    static_target = str(apkpath) #this must be the complete path of apk file
    targetapp = Target(static_target)
    if targetapp.package_name is not None:
        session_name = targetapp.package_name #usare md5, meglio
    else:
        session_name = "dummyname"
    #first we need to check if a cache file already exists
    #targetapp.save_session(core.myglobals.dissector_global_dir  + "/cache/" + session_name + '.andro')
    manifestInfo = Manifest(targetapp)
    manifestAnalysis = ManifestAnalyzer(manifestInfo,targetapp);

    print "Writing new JSON file with permissions..."
    #Should appear a new file called [files/permissions.json]
    print "Writing new JSON file with pscout mappings..."
    #Should appear a new file called []
    manifestInfo.checkPermissions(config.version, apkpath, config.outputdir)

    #deob = Deobfuscator(targetapp)
    #vmfilter = VirtualMethodsFilter(manifestAnalysis)
    #writer = HookWriter(manifestAnalysis,vmfilter)
    #writer.write(dest+'Fuffa.java')
    #print 'scritto'

def analyzeSample(samplepath, config):
    runningThreads = 0
    i = 0
    apks = os.listdir(samplepath)
    threadList = list()
    for apk in apks:
        if runningThreads < config.threads:
            #Generating apk path
            apkpath = ""
            if samplepath[:-1] is "/":
                apkpath = samplepath + apk
            else:
                apkpath = samplepath + "/" + apk

            param = prepareParameters(apkpath,config)
            t = threading.Thread(target=analyzeAPK(), args=param)
            threadList.append(t)
            t.start()   #Starting new thread
            i += 1
        else:
            #Wait until all threads are finished
            for thread in threadList:
                thread.join()
            threadList = list() #Clear list that contains finished threads
            #Launch thread of this iteration and append to our threadList
            param = prepareParameters(apkpath,config)
            t = threading.Thread(target=analyzeAPK(), args=param)
            threadList.append(t)
            t.start()
            i=1

def prepareParameters(apkpath,config):
    param = list()
    list.append(config.version)
    list.append(apkpath)
    list.append(config.outputdir)
    return param

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