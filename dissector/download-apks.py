__author__ = 'sergio'
import os, time, optparse, requests, json

def print_help(parser):
    print "arguments error!!\n"
    parser.print_help()
    exit(-1)

def main(key,file,type):
    #Read file
    if not os.path.isfile(file):
        print "arguments error!!\n"
        exit(-1)
    #Create new directory for the downloads
    #pwd = os.getcwd()
    path = "/tmp/virustotal/sd1/"
    if not os.path.exists(path):
        print "Creating new dir " + path
        os.makedirs(path)

    if type is "json":
        jsonoption(key,file,path)

    else:
        txtoption(key,file,path)

def jsonoption(key,file,path):
    with open(file,"r") as data_file:
        jsonarray = json.load(data_file)

    #Reading each element
    i = 0
    success = 0
    while i < len(jsonarray["notifications"]):
        apk = jsonarray["notifications"][i]["sha1"]
        result = download(key,apk)
        if result is not None:
            apkfile = open(path + apk+".apk",'w')
            apkfile.write(result)
            success += 1
        i += 1

    print "Total apks: " + str(i) + " Downloaded apks: " + str(success)

def txtoption(key,file,path):
    i = 0
    success = 0
    with open(file,"r") as f:
        apk = f.readline()
        result = download(key,apk)
        if result is not None:
            print "Chaging apk name"
            apkfile = open(path+apk+".apk",'w')
            apkfile.write(result)
            success += 1
        i += 1

    print "Total apks: " + str(i) + " Downloaded apks: " + str(success)


def download(key,apk):
    print "Downloading apk: " + str(apk)
    params = {'apikey': key, 'hash': apk}
    response = requests.get('https://www.virustotal.com/vtapi/v2/file/download', params=params)
    i = 0
    while i < 3 and response.status_code is not 200:
        print "Trying " + str(i+1) + " attempt"
        time.sleep(2)
        response = requests.get('https://www.virustotal.com/vtapi/v2/file/download', params=params)
        i += 1
    print "CODE: " + str(response.status_code)
    element = response.content
    if response.status_code is 200:
        return element
    else:
        return None

if __name__ == "__main__":
    #Parameters
    # 1 -> Your API key
    # 2 -> Your file .txt which has a list of hashes

    parser = optparse.OptionParser()
    parser.add_option('-k', '--key' , action="store", help="Your API key", dest="key",type='string')
    parser.add_option('-f','--file', action="store", help="[OPTIONAL] Your .txt file which has a list of hashes",
                      dest="txtfile",type='string'),
    parser.add_option('-j','--json', action="store", help="[OPTIONAL] Your json file which has a list of hashes",
                      dest="jsonfile",type='string')

    (opts, args) = parser.parse_args()
    if opts.key is None:
        print_help(parser)
    if opts.txtfile is None:
        main(opts.key,opts.jsonfile,"json")
    if opts.jsonfile is None:
        main(opts.key,opts.txtfile,"txt")

