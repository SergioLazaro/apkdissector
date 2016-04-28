__author__ = 'sergio'

import requests, optparse, os

def main(opts):
    #Write N apk hashes
    if opts.write is not None and opts.num is not None:
        #Limiting the number of apks to download
        if opts.num < 1000000:  #Number should be lower than 1 million
            writehashes(opts.num)
        else:
            print "[!!] -n arg should be lower than 1 million."
            exit(-1)


def writehashes(num):
    #Get petition to the first page
    next_url = 'https://api.koodous.com/apks'
    print "Your hashes.txt file is in " + os.getcwd() + "/files/"
    fd = open('files/hashes.txt','w')
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
                print apk['sha256']
                i += 1
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

    parser.add_option('-w', '--write', default=True, help="Write N apk hashes in a TXT file",
                       dest="verbose",type='string')

    parser.add_option('-f','--file', action="store", help="TXT file which contains hashes to download.",
                      dest="hashesfile",type="string")

    parser.add_option('-s','--sample',action="store", help="TXT file which contains a sample of Koodous API keys.",
                      dest="keyfile",  type="string")

    parser.add_option('-k','--key',action="store", help="Koodus key to download a sample allowed.",
                      dest="key", type="string")

    (opts, args) = parser.parse_args()
    if opts.num is None and opts.write is None and opts.hashesfile is None and opts.keyfile is None and \
                    opts.sample is None and opts.key is None:
        print_help(parser)
    else:
        if opts.help is not None:
            print_help(parser)
        else:
            #main(opts)
            print opts