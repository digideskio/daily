#!/usr/bin/env python

# need youtube-dl

import pafy
import sys
import re
import urllib2
import os.path

import requests

# download individual videos
def download_all(urls):
    for url in urls:
        print "downloading:", url 
        try:
            best     = url.getbest()
            fullName = url.title + "." + best.extension
            if not os.path.isfile(fullName):
                best.download()
        except IndexError as e:
            print e
        except urllib2.HTTPError as e:
            print e
        except KeyError as e:
            print e
#targets = sys.argv[1:]
#targets = map(str, targets)

if len(sys.argv) <= 1:
    with open('./input.list') as f:
        targets = f.readlines()
else:
    targets = sys.argv[1:]
    targets = map(str, targets)

urls    = []
for target in targets:
    playlist = re.search(r"playlist", target)
    if playlist:
        list_content = pafy.get_playlist(target)['items']
        urls += map(lambda x: x['pafy'], list_content)
    else:
        urls.append(pafy.new(target))

print urls
download_all(urls)
