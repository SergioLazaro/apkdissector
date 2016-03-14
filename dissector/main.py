__author__ = 'vaioco'

from collector.manifest import Manifest
from core.target import Target
from analyzer.manifest import ManifestAnalyzer
from analyzer.deobfuscator import Deobfuscator
from core.filters import VirtualMethodsFilter
from core.writers import HookWriter
#import sys
#sys.path.insert(1, '/Users/vaioco/android_stuff/androguard')

static_target = '/Users/vaioco/ownCloud/documents/Dottorato/ProgettoPhd/art-hooking-vtable/examples/testing-app.apk'  #'/Users/vaioco/Lavoro/cert/youapp/base.apk'

dest = '/Users/vaioco/ownCloud/documents/Dottorato/ProgettoPhd/apkdissector/'
cache_dir = '/Users/vaioco/ownCloud/documents/Dottorato/ProgettoPhd/apkdissector/cache/'

def main():
    print 'Analizzo il manifest'

    targetapp = Target(static_target)
    if targetapp.package_name is not None:
        session_name = targetapp.package_name #usare md5, meglio
    else:
        session_name = "dummyname"
    targetapp.save_session(cache_dir+session_name+'.andro')
    manifestInfo = Manifest(targetapp)
    manifestAnalysis = ManifestAnalyzer(manifestInfo,targetapp);
    deob = Deobfuscator(targetapp)
    vmfilter = VirtualMethodsFilter(manifestAnalysis)
    writer = HookWriter(manifestAnalysis,vmfilter)
    writer.write(dest+'Fuffa.java')
    print 'scritto'




if __name__ == "__main__":
    main()