__author__ = 'sergio'

import os,optparse, json
from decimal import Decimal
from core.statistics import Statistics

class PermissionCount:

    def __init__(self,permission,count):
        self.permission = permission
        self.count = count

def statisticsFromFiles(dir):
    if dir[-1:] is not "/":
        dir = dir + "/"
    if os.path.isdir(dir):
        statistics = Statistics(dir)
        statistics.getStatisticsFromFiles()

def statisticsFromDB(database):
    if os.path.isfile(database):
        statistics = Statistics(database)
        statistics.getStatisticsFromDB()


def print_help(parser):
    print "arguments error!!\n"
    parser.print_help()
    exit(-1)

if __name__ == "__main__":
    #Parameters
    # 1 -> Path to your directory with APKs analyzed

    parser = optparse.OptionParser()
    parser.add_option('-d', '--dir' , action="store", help="Path to your directory with APKs analyzed i.e:/path/to/your/apk/analyzed/",
                      dest="dir",type='string')
    parser.add_option('-b', '--database', action="store", help="Path to your database with analyzed apks",
                      dest="database", type="string")

    (opts, args) = parser.parse_args()

    if opts.dir is not None and os.path.isdir(opts.dir):
        statisticsFromFiles(opts.dir)
    elif opts.database is not None:
        statisticsFromDB(opts.database)

    else:
        print_help(parser)