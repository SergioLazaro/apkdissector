import os

__author__ = 'sergio'

import optparse
from enforcement.fixer import Fixer
from enforcement.permMapParser import AndroidJsonParser
from enforcement.permStackDb import PermStackDb
from enforcement.dbMapper import DbMapper

'''
    Method called when all the options are setted up.
'''
def main(jsonpath,permission,dbpath,jsondb):

    reader = Fixer(jsonpath)        #Fixing the json file if is not well formed

    jsoninfo = AndroidJsonParser(jsonpath)  #Parsing the JSON file
    print "[*] Total elements read: " + str(len(jsoninfo.permissionStackElementList))
    print "[*] Creating SQLite database to store the information..."
    permStackDB = PermStackDb(jsoninfo.permissionStackElementList,jsondb,permission)

    #SHOULD CONTINUE WITH MORE OPTIONS CODE

    print "[*] Execution finished successfuly"

'''
    Method called when the options [-p] and [-j] are setted up
'''
def jsonDBpermissionCheck(permission,jsondb):
    permStackDB = PermStackDb(None,jsondb,permission)

'''
    Method called when the options [-f], [-j] and [-p] are
    setted up. This function is also called when [-f] and
    [-j] are setted up, without [-p]
'''
def createjsonDBandCheckPermission(jsonpath,jsondb,permission):
    print "[*] Checking if JSON file is well formed..."
    reader = Fixer(jsonpath)        #Fixing the json file if its not well formed

    if os.path.isDir(jsonpath):
        #Directory option
        for elem in os.listdir(jsonpath):
            if elem.endswith(".json"):
                print "[*] Reading JSON file..."
                jsoninfo = AndroidJsonParser(jsonpath)  #Parsing the JSON file
                print "[*] Total elements read: " + str(len(jsoninfo.permissionStackElementList))
                print "[*] Creating SQLite database to store the information..."
                permStackDB = PermStackDb(jsoninfo.permissionStackElementList,jsondb,permission)
    else:
        #File option
        print "[*] Reading JSON file..."
        jsoninfo = AndroidJsonParser(jsonpath)  #Parsing the JSON file
        print "[*] Total elements read: " + str(len(jsoninfo.permissionStackElementList))
        print "[*] Creating SQLite database to store the information..."
        permStackDB = PermStackDb(jsoninfo.permissionStackElementList,jsondb,permission)

def checkPermissionBothDBs(jsondb,pscoutdb,permission):
    map = DbMapper(jsondb,pscoutdb,permission)

def print_help(parser):
    parser.print_help()
    print "COMMAND HELP EXAMPLES:\n"
    print "1) Parse JSON file and create a DB"
    print "\tpython enforcementParser.py -f json/file/path.json -j /output/directory/\n"
    print "2) Parse JSON file, create DB and check a permission"
    print "\tpython enforcementParser.py -f json/file/path.json -j /output/directory/ -p android.permission.READ_PHONE_STATE\n"
    print "3) Check a permission on a created database"
    print "\tpython enforcementParser.py -j /path/json/database.db -p android.permission.READ_PHONE_STATE\n"
    print "4) Check permission mapping with PScout DB and JSON DB"
    print "\tpython enforcementParser.py -j /path/json/database.db -d /path/pscout/pscout.db -p android.permission.READ_PHONE_STATE\n"
    exit(-1)

if __name__ == "__main__":

    parser = optparse.OptionParser()
    parser.add_option('-f', '--file(s)', action="store", help="Path to JSON file or directory with JSONs", dest="file",type="string"),
    parser.add_option('-p','--perm', action="store", help="Full permission name to analyze", dest="permission",type="string"),
    parser.add_option('-d', '--db', action="store", help="PScout DB path", dest="dbpath",type="string"),
    parser.add_option('-j', '--jsondb', action="store", help="SQLite DB path to put it or path to a existing SQLite DB",
                      dest="jsondb",type="string")

    (opts, args) = parser.parse_args()
    if opts.jsondb is not None:

        if opts.file is not None and opts.permission is not None:
            createjsonDBandCheckPermission(opts.file,opts.jsondb,opts.permission)

        elif opts.file is not None:
            createjsonDBandCheckPermission(opts.file,opts.jsondb,None)
        else:
            print_help(parser)

    elif opts.permission is not None and opts.jsondb is not None:
        if opts.dbpath is not None:
            #Compare jsonDB (self created) with the PScout DB
            checkPermissionBothDBs(opts.jsondb,opts.dbpath,opts.permission)
        else:
            #Check db and print
            jsonDBpermissionCheck(opts.permission, opts.jsondb)

    elif opts.file is not None and opts.permission is not None and opts.dbpath is not None and opts.jsondb is not None:
        main(opts.file,opts.permission,opts.dbpath,opts.jsondb)

    else:
        print_help(parser)