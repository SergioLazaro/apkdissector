__author__ = 'sergio'

import optparse
from enforcement.enforceReader import Reader
from enforcement.permMapParser import AndroidJsonParser
from enforcement.permStackDb import PermStackDb

def main(jsonpath,permission,dbpath,output):

    reader = Reader(jsonpath,dbpath)
    #reader.checkPermissionInfo(permission)
    jsoninfo = AndroidJsonParser(jsonpath)
    print "[*] Total elements read: " + str(len(jsoninfo.permissionStackElementList))
    print "[*] Creating SQLite database to store the information..."
    permStackDb = PermStackDb(jsoninfo.permissionStackElementList,output)
    print "[*] Execution finished successfuly"

def print_help(parser):
    print "arguments error!!\n"
    parser.print_help()
    exit(-1)

if __name__ == "__main__":

    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', action="store", help="Enforce permission JSON file path", dest="file",type="string"),
    parser.add_option('-p','--perm', action="store", help="Full permission name to analyze", dest="permission",type="string"),
    parser.add_option('-d', '--db', action="store", help="PScout DB path", dest="dbpath",type="string"),
    parser.add_option('-o', '--output', action="store", help="SQLite DB generated with JSON file content ", dest="output",
                      type="string")

    (opts, args) = parser.parse_args()
    if opts.file is not None and opts.permission is not None and opts.dbpath is not None and opts.output is not None:
        main(opts.file,opts.permission,opts.dbpath,opts.output)
    else:
        print_help(parser)