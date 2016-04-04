import os,optparse

from decimal import Decimal

__author__ = 'sergio'

class PermissionCount:

    def __init__(self,permission,count):
        self.permission = permission
        self.count = count


def main(dir):
    apks = os.listdir(dir)
    results = list()
    for i,val in enumerate(apks):
        apkpath = dir+val
        if os.path.isdir(apkpath):
            print "ITEM: " + str(i) + " VALUE: " + val + " IS DIR"
            permissions = os.listdir(apkpath)
            print permissions
            print "LENGTH: " + str(len(results))
            results = updateResult(results,permissions)
            print "LENGTH: " + str(len(results))

    print "Total apks: " + str(i)
    print "============================================================"
    printStatistics(results,i)

def printStatistics(results,i):
    for val in results:
        print "PERMISSION: " + val.permission + " VALUE: " + str(val.count) + " PERCENTAGE: " +\
              str(Decimal(val.count)/Decimal(i))

def updateResult(results, permissions):
    for tmppermission in permissions:
        position = -1
        for i,existingpermission in enumerate(results):
            if existingpermission.permission == tmppermission:
                position = i

        if position == -1:  #tmppermission does not exists
            #Create new PermissionCount
            p = PermissionCount(tmppermission,1)
            #Append new PermissionCount
            results.append(p)
            print "Added new permission: " + p.permission + " VALUE: 1"
        else:           #tmppermission exists so we have to increment the value
            p = results[position]
            p.count += 1
            print "Permission: " + p.permission + " NEW VALUE: " + str(p.count)
    return results


    return results

def print_help(parser):
    print "arguments error!!\n"
    parser.print_help()
    exit(-1)

if __name__ == "__main__":
    #Parameters
    # 1 -> Path to your directory with APKs analyzed

    parser = optparse.OptionParser()
    parser.add_option('-d', '--dir' , action="store", help="Path to your directory with APKs analyzed",
                      dest="dir",type='string')

    (opts, args) = parser.parse_args()
    if opts.dir is None or (not os.path.isdir(opts.dir)):
        print_help(parser)
    else:
        main(opts.dir)