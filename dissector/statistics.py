__author__ = 'sergio'

import os,optparse, json
from decimal import Decimal
from core.statistics import Statistics

class PermissionCount:

    def __init__(self,permission,count):
        self.permission = permission
        self.count = count

def main(dir):
    if os.path.isdir(dir):
        statistics = Statistics(dir)
        statistics.getStatistics()


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

    (opts, args) = parser.parse_args()
    if opts.dir is None or (not os.path.isdir(opts.dir)):
        print_help(parser)
    else:
        main(opts.dir)
