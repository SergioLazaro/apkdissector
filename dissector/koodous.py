__author__ = 'sergio'

import requests, optparse, os, urllib

def main(opts):
    #Write N apk hashes
    if opts.writefile is not None and opts.num is not None:
        #Limiting the number of apks to download
        if opts.num < 1000000:  #Number should be lower than 1 million
            writehashes(opts.num, opts.writefile)
        else:
            print "[!!] -n arg should be lower than 1 million."
            exit(-1)
    elif opts.key is not None and opts.hashesfile is not None:
        downloadAPKS(opts.key, opts.hashesfile, 0)

    elif opts.keyfile is not None and opts.hashesfile is not None:
        samplekeysdownload(opts.keyfile,opts.hashesfile)

'''
    Method used to download a sample of APKS using differents API key
    inside a file. The method read the hashes file for each key and take
    care of downloading the same APK twice or more.
'''
def samplekeysdownload(keysfile,hashesfile):
    downloadedapks = 0
    with open(keysfile,'w') as fd:
        keys = fd.readlines()
        for key in keys:
            print "[*] Using key " + key + " ..."
            key = key.rstrip('\n')
            downloadedapks = downloadAPKS(key,hashesfile,downloadedapks)

'''
    Download APKS using an API key until the server response
    to the get petition with a response_code different to 200 (OK).
    When it has finished, returns the number of APKS downloaded.
'''
def downloadAPKS(key, hashes, downloadedapks):
    #Checking if destination directory exists
    if not os.path.exists('/tmp/koodous/'): #If not, we create it
        os.makedirs('/tmp/koodous/')

    exit = False
    print "[*] Opening file " + hashes
    with open(hashes,'w') as fd:
        lines = fd.readlines()
        while not exit:         #Iterate until the API restrict the downloads (at least 50)
            hash = lines[downloadedapks].rstrip('\n') #Cleaning the \n
            print "[*] Downloading " + hash() + " ..."
            exit = downloadSingleAPK(hash,key)  #Call to download APK
            downloadedapks += 1
    return downloadedapks

'''
    Download an APK using an API key. Returns True if (and only if)
    the request has a response_code different to 200 (OK). That uses
    to mean that the key cant be used more that day.
'''
def downloadSingleAPK(hash,key):
    url_koodous = "https://api.koodous.com/apks/%s/download" % hash
    r = requests.get(url=url_koodous, headers={'Authorization': key})
    exit = False
    if r.status_code is 200:
        fd = open('/tmp/koodous/' + hash + '.apk','w')
        testfile = urllib.URLopener()
        testfile.retrieve(r.json().get('download_url'), fd)
        fd.close()
        print "[*] " + hash + " downloaded successfuly"
    else:
        exit = True
        print "[!!] Error while trying to download " + hash + " code = " + r.status_code

    return exit

'''
    Method use to ask for JSON responses. It iterates until it has N hashes wrote in a file.
    It parses the JSON response to get the next URL to ask for the new JSON file and reads N
    hashes wrote in that JSON. If N > 50, it will iterate until it has finished.
    
'''
def writehashes(num,file):
    #Get petition to the first page
    next_url = 'https://api.koodous.com/apks'
    print "[*] Writing hashes in " + file
    fd = open(file,'w')
    i = 0

    while (i < num) or (i == int(-1)):
        #Requesting next json response
        print "[*] Requesting new JSON file to " + next_url
        r = requests.get(url=next_url, headers={})
        if r.status_code is 200:    #Correct work flow
            json = r.json()
            #Getting next url to get next json response
            next_url = json['next']
            apks = json['results']  #Getting info about 50 apks
            for apk in apks:
                fd.write(apk['sha256'] + "\n")  #Writing on the file
                i += 1
            print "[*] " + str(i) + " APKS written."
        else:                       #If the status_code is not 200
            i = -1                  #we exit the loop
            print "[*] Requested URL response code is not 200."
            print "[*] Exiting..."

def print_help(parser):
    print "arguments error!!\n"
    parser.print_help()
    exit(-1)

if __name__ == "__main__":
    #Parameters
    # -n -> Number of hashes to download.
    # -w -> Write N apk hashes in a TXT file.
    # -f -> TXT file which contains hashes to download.
    # -s -> TXT file which contains a sample of Koodous API keys
    # -k -> Koodus key to download a sample allowed.

    parser = optparse.OptionParser()

    parser.add_option('-n', '--num' , action="store", help="Number of hashes to download.",
                      dest="num",type='string')

    parser.add_option('-w', '--write', action="store", help="Write N apk hashes in a TXT file",
                       dest="writefile",type='string')

    parser.add_option('-f','--file', action="store", help="TXT file which contains hashes to download.",
                      dest="hashesfile",type="string")

    parser.add_option('-s','--sample',action="store", help="TXT file which contains a sample of Koodous API keys.",
                      dest="keyfile",  type="string")

    parser.add_option('-k','--key',action="store", help="Koodus key to download a sample allowed.",
                      dest="key", type="string")

    (opts, args) = parser.parse_args()
    if (opts.num is None and opts.writefile is None) or (opts.hashesfile is None and opts.keyfile is None) or \
            (opts.hashesfile is None and opts.key is None):
        print_help(parser)
    else:
        main(opts)