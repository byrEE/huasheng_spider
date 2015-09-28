#!/usr/bin/env python3
# coding=utf-8
from urllib import request
import re
from bs4 import BeautifulSoup
from get_ua import get_ua

#start_url='http://bbs.voc.com.cn/topic-6773443-1-1.html'
start_url='http://bbs.voc.com.cn/topic-6777711-1-1.html'
pattern_img=re.compile(r'http://image.hnol.net.*?jpg')
def url_img(url):
    req=request.Request(url)
    req.add_header('user-agent',get_ua())
    with request.urlopen(req) as imgpage:
        data=imgpage.read().decode('gbk')
        soup=BeautifulSoup(data,'lxml')
        img_url=soup.find_all('a',href=pattern_img)
        img_m=[]
        for item in img_url:
            m1=re.findall(pattern_img,str(item))
            img_m.append(m1[0])
        with open('img_url.txt','w') as fimg:
            fimg.write(str(img_m))

if __name__=='__main__':
    url_img(start_url)
