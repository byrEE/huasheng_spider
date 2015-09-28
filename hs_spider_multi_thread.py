#!/usr/bin/env python3
# coding=utf-8
from urllib import request
from bs4 import BeautifulSoup
from get_ua import get_ua
import re
from collections import deque
class hs_spider(object):
    def __init__(self):
        #start_url='http://bbs.voc.com.cn/forum-50-2.html'
        self.head_url='http://bbs.voc.com.cn/'
        #self.forum='forum-'
        #forum_id=
        self.pattern_topic=re.compile(r'(topic.*?html)')
        self.pattern_dl=re.compile(r'.*?/\w/.*?/\d+/\d+/(\d+-\d+.jpg)')
        self.pattern_img=re.compile(r'http://image.hnol.net.*?jpg')
        self.queue_topic=deque()
        self.queue_img=deque()


    def set_forum_id(self,id):
        self.forum_id=id

    def get_forum_url(self):
        return 'forum-'+str(self.forum_id)+'-'

    def url_parse(self,parsing_url):
        req=request.Request(parsing_url)
        req.add_header('user-agent',get_ua())
        with request.urlopen(parsing_url) as f:
            data=f.read().decode('gbk')
            soup=BeautifulSoup(data,'lxml')
            return soup


    def url_parse_topic(self,soup_topic):
        #req=request.Request(url_topic)
        #req.add_header('user-agent',get_ua())
        #with request.urlopen(req) as fpage:
            #data=fpage.read().decode('gbk')
            #soup=BeautifulSoup(data,'lxml')
        topic_url=soup_topic.find_all('a',href=self.pattern_topic)
            #topic_m=[]
        for item in topic_url:
            m1=re.findall(self.pattern_topic,str(item))
            self.queue_topic().append(m1[0])
                #print(m1[0])
                #topic_m.append(m1[0])
                #topic_url=soup.find_all(text=pattern)
                #print(topic_url)
            #with open('topic.txt','w') as f:
                #f.write(str())

    def url_parse_img(self,soup_img):
        #req=request.Request(url)
        #req.add_header('user-agent',get_ua())
        #with request.urlopen(req) as imgpage:
            #data=imgpage.read().decode('gbk')
            #soup=BeautifulSoup(data,'lxml')
        img_url=soup_img.find_all('a',href=self.pattern_img)
        #img_m=[]
        for item in img_url:
            m1=re.findall(self.pattern_img,str(item))
            self.queue_img.append(m1[0])
        #with open('img_url.txt','w') as fimg:
            #fimg.write(str(img_m))


    def dl_img(self,url_img):
        m=re.findall(self.pattern_dl,url_img)[0]
        #print(m)
        #print(filename)
        with request.urlopen(url_img) as f:
            data=f.read()
            with open(m,'wb') as img:
                img.write(data)


    def savePageInfo(self,pageIndex):
        page_url=self.head_url+self.get_forum_url()+pageIndex+'.html'
        soup_tmp=self.url_parse(page_url)
        self.url_parse_topic(soup_tmp)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    def getPagesInfo(self,start,end):
        for i in range(start,end+1):
            self.savePageInfo(i)
