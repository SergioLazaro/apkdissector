__author__ = 'sergio'

import requests, urllib

def main():
    #Get petition to the first page
    url_apks = 'https://api.koodous.com/apks'
    r = requests.get(url=url_apks, headers={})
    fd = open('files/hashes.txt','w')
    i = 0
    if r.status_code is 200:
        while i < 10000:
            json = r.json()
            #Getting next url to get next json response
            nexturl = json['next']
            apks = json['results']  #Getting info about 50 apks
            for apk in apks:
                fd.write(apk['sha256'] + "\n")  #Writing on the file
                print apk['sha256']
                i += 1
            #Requesting next json response
            r = requests.get(url=nexturl, headers={})
            if r.status_code is not 200:    #If the status_code is not 200
                i = 10001                   #we exit the loop
                
main()