__author__ = 'sergio'
import optparse
import sqlite3

def main(file,outputpath, version):
    if outputpath[-1:] is not "/":
        outputpath = outputpath + "/"
    outputpath = outputpath + version + ".db"
    print "DB path: " + outputpath
    print "Creating new DB..."
    conn = sqlite3.connect(outputpath)
    conn.execute(''' DROP TABLE IF EXISTS %s''' % ("pscout"))
    query1 = '''
    CREATE TABLE %s
           (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
           CALLERCLASS             VARCHAR,
           CALLERMETHOD            VARCHAR,
           CALLERMETHODDESC        VARCHAR,
           PERMISSION              VARCHAR,
           VERSION                 VARCHAR);
    ''' % ("pscout")
    conn.execute(query1)

    with open(file) as file:
        i = 1
        for line in file:
            list = line.split(",")
            #print "Added record: %d\n" % (i)
            #print "%s - %s - %s - %s - %s\n" % (list[0],list[1],list[2],list[3],list[4])
            conn.execute("INSERT INTO pscout (CALLERCLASS,CALLERMETHOD,CALLERMETHODDESC,PERMISSION,VERSION) "
                         "VALUES (?,?,?,?,?)",(list[0],list[1],list[2],list[3],list[4]));

        conn.commit()
        print "[*] DB created successfully in " + outputpath;
    conn.close()

def print_help(parser):
    print "arguments error!!\n"
    parser.print_help()
    exit(-1)

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-f','--file', action="store", help="PSCout project CSV file ", dest="file",type="string")
    parser.add_option('-o','--outputdir', action="store", help="Output directory where the db file will be stored ",
                      dest="outputdir",type="string"),
    parser.add_option('-v','--version', action="store", help="PSCout version", dest="version",type="string")

    (opts, args) = parser.parse_args()
    if opts.file is None and opts.outputdir is None and opts.version is None:
        print_help(parser)
    else:
        main(opts.file, opts.outputdir, opts.version)