__author__ = 'vaioco'

from collector.manifest import Manifest
from core.target import Target
from analyzer.manifest import ManifestAnalyzer
from analyzer.deobfuscator import Deobfuscator
from core.filters import VirtualMethodsFilter
from core.writers import HookWriter
import sys
import optparse
import core.myglobals
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
def main(version, apkpath, destinationpath):
    global dissector_global_dir
    print 'Analizzo il manifest'
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
    manifestInfo.checkPermissions(version, apkpath, destinationpath)



    #deob = Deobfuscator(targetapp)
    #vmfilter = VirtualMethodsFilter(manifestAnalysis)
    #writer = HookWriter(manifestAnalysis,vmfilter)
    #writer.write(dest+'Fuffa.java')
    #print 'scritto'

def print_help(parser):
    print "arguments error!!\n"
    parser.print_help()
    exit(-1)

if __name__ == "__main__":
    #ARG0: version of android for checking pscout version file
    #ARG1: APK name, always without the extension
    #ARG2: Directory where you want to write the files
    #      and also, where the PScout files and db (if exists) should be
    core.myglobals.init()
    print core.myglobals.dissector_global_dir
    parser = optparse.OptionParser()
    parser.add_option('-v', action="store", help="Android version to compare with", dest="pscoutversion",type='string')
    parser.add_option('-i', action="store", help="apk file without the extensions", dest="inputapk",type='string')
    parser.add_option('-o', action="store", help="Working directory", dest="outdir",type='string')

    (opts, args) = parser.parse_args()
    if opts.pscoutversion is None or opts.inputapk is None or opts.outdir is None:
        print_help(parser)
    #print opts, args
    main(opts.pscoutversion,opts.inputapk,opts.outdir)