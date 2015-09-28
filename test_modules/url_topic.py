#!/usr/bin/env python3
# coding=utf-8
from urllib import request
from bs4 import BeautifulSoup
from get_ua import get_ua
import re
start_url='http://bbs.voc.com.cn/forum-50-2.html'
head_url='http://bbs.voc.com.cn/'
pattern_topic=re.compile(r'(topic-6.*?html)')
def url_parse_topic(url):
    req=request.Request(url)
    req.add_header('user-agent',get_ua())
    with request.urlopen(req) as fpage:
        data=fpage.read().decode('gbk')
        soup=BeautifulSoup(data,'lxml')
        topic_url=soup.find_all('a',href=pattern_topic)
        topic_m=[]
        for item in topic_url:
            m1=re.findall(pattern_topic,str(item))
            #print(m1[0])
            topic_m.append(m1[0])
        #topic_url=soup.find_all(text=pattern)
        #print(topic_url)
        with open('jieguo.txt','w') as f:
            f.write(str(topic_m))

if __name__=='__main__':
    url_parse_topic(start_url)
