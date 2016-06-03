#!/usr/bin/env python

import requests
import mechanize
import cookielib

import re
import wget

import subprocess
import time

import sys
import urllib2

# download a video on the page
def download_video(url):
    while True:
        try:
            response = br.open(url)
            break
        except urllib2.URLError:
            print "Error in find video_url"
            time.sleep(10)
    doc    =  response.read()
    TAG_ID = 'download_link'

    m  = re.search("video_url: '(\S+)/\?br\S+',", doc)
    video_url = m.group(1)
    print video_url
    subprocess.call(["wget", "-c", "-t 0",
                     "--timeout=60", "--waitretry=60",
                     video_url])


br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


if len(sys.argv) <= 1:
    with open("ARCHIVE.txt", "r") as f:
        archive = f.readlines();

    with open("TODO.txt", "r") as f:
        lines = f.readlines();

    for line in lines:
        download_video(line)
        with open("ARCHIVE.txt", "a") as f:
            f.write(line)
else:
    for line in sys.argv[1:]:
        download_video(line)
