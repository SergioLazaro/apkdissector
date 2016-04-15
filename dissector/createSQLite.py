__author__ = 'sergio'
import optparse
import sqlite3

def main(file,version):
    print "Creating new DB in /tmp/"
    conn = sqlite3.connect('/tmp/permissions.db')
    conn.execute(''' DROP TABLE IF EXISTS %s''' % ("permissions"))
    query1 = '''
    CREATE TABLE %s
           (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
           CALLERCLASS             VARCHAR,
           CALLERMETHOD            VARCHAR,
           CALLERMETHODDESC        VARCHAR,
           PERMISSION              VARCHAR,
           VERSION                 VARCHAR);
    ''' % ("permissions")
    conn.execute(query1)

    with open(file) as file:
        i = 1
        for line in file:
            list = line.split(",")
            print "Added record: %d\n" % (i)
            print "%s - %s - %s - %s - %s\n" % (list[0],list[1],list[2],list[3],list[4])
            conn.execute("INSERT INTO permissions (CALLERCLASS,CALLERMETHOD,CALLERMETHODDESC,PERMISSION,VERSION) "
                         "VALUES (?,?,?,?,?)",(list[0],list[1],list[2],list[3],list[4]));

        conn.commit()
        print "Records created successfully";
    conn.close()

def print_help(parser):
    print "arguments error!!\n"
    parser.print_help()
    exit(-1)

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-v', '--version', action="store", help="PScout version", dest="version",type="string")
    parser.add_option('-f','--file', action="store", help="PSCout project CSV file ", dest="file",type="string")

    (opts, args) = parser.parse_args()
    if opts.file is None and opts.version:
        print_help(parser)
    else:
        main(opts.file, opts.version)