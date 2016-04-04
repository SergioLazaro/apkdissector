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
            results = updateResult(results,permissions)

    print "Total apks: " + str(i)
    print "============================================================"
    printStatistics(results,i+1,dir)

def printStatistics(results,i,dir):
    for val in results:
        percentage = (Decimal(val.count)/Decimal(i))*100
        print("PERMISSION: %s VALUE: %d PERCENTAGE: %.2f%%") % (val.permission,val.count, percentage)

    response = raw_input("Do you want a JSON file?[Y/N]: ")
    if response is "Y" or response is "y":
        generateJSON(results,i,dir)

def generateJSON(results,i,dir):
    fd = open(dir+"statistics.json","w")
    fd.write('{"permissions": [')
    for j,val in enumerate(results):
        percentage = (Decimal(val.count)/Decimal(i))*100
        if j < len(results) - 1:
            fd.write('{"permission":"' + val.permission + '","count":"' + str(val.count) +
                     '",percentage":"' + str(percentage) + '"},')
        else:
            fd.write('{"permission":"' + val.permission + '","count":"' + str(val.count) +
                     '",percentage":"' + str(percentage) + '"}')
    fd.write("]}")

        #print("PERMISSION: %s VALUE: %d PERCENTAGE: %.2f%%") % (val.permission,val.count, percentage)
    fd.close()



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
        else:           #tmppermission exists so we have to increment the value
            p = results[position]
            p.count += 1
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