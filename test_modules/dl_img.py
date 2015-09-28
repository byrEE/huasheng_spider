#!/usr/bin/env python3
# coding=utf-8
from urllib import request
import re

start_url='http://image.hnol.net/c/2015-09/23/11/201509231128463691-2285289.jpg'
dl_pattern=re.compile(r'.*?/\w/.*?/\d+/\d+/(\d+-\d+.jpg)')
def dl_img(url):
    m=re.findall(dl_pattern,url)[0]
    print(m)
    #print(filename)
    with request.urlopen(url) as f:
        data=f.read()
        with open(m,'wb') as img:
            img.write(data)

if __name__=='__main__':
    dl_img(start_url)
