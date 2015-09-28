#!/usr/bin/env python3
# coding=utf-8
from urllib import request
from bs4 import BeautifulSoup
from get_ua import get_ua
import re
import os


#from collections import deque
class hs_spider(object):
    def __init__(self):
        #start_url='http://bbs.voc.com.cn/forum-50-2.html'
        self.head_url='http://bbs.voc.com.cn/'
        #self.forum='forum-'
        #forum_id=
        self.pattern_topic=re.compile(r'(topic-6.*?html)')
        self.pattern_dl=re.compile(r'.*?/\w/.*?/\d+/\d+/(\d+-\d+.jpg)')
        self.pattern_img=re.compile(r'http://image.hnol.net.*?jpg')
        #self.queue_topic=deque()
        #self.queue_img=deque()


    def set_forum_id(self,id):
        self.forum_id=id

    def get_forum_url(self):
        return 'forum-'+str(self.forum_id)+'-'

    def url_parse(self,parsing_url):
        req=request.Request(parsing_url)
        req.add_header('user-agent',get_ua())
        #try:
        with request.urlopen(parsing_url) as f:
            data=f.read().decode('gbk')
            soup=BeautifulSoup(data,'lxml')
            return soup
        #except:
            #None


    def url_parse_topic(self,url_topic):
        req=request.Request(url_topic)
        req.add_header('user-agent',get_ua())
        with request.urlopen(req) as fpage:
            data=fpage.read().decode('gbk')
            soup_topic=BeautifulSoup(data,'lxml')
            topic_url=soup_topic.find_all('a',href=self.pattern_topic)
            topic_m=[]
            for item in topic_url:
                m1=re.findall(self.pattern_topic,str(item))
                topic_m.append(m1[0])
            return topic_m
                #print(m1[0])
                #topic_m.append(m1[0])
                #topic_url=soup.find_all(text=pattern)
                #print(topic_url)
            #with open('topic.txt','w') as f:
                #f.write(str())

    def url_parse_img(self,url):
        req=request.Request(url)
        print(url)
        req.add_header('user-agent',get_ua())
        with request.urlopen(req) as imgpage:
            data1=imgpage.read().decode('gbk')
            soup_img=BeautifulSoup(data1,'lxml')
            img_url=soup_img.find_all('a',href=self.pattern_img)
            img_m=[]
            for item in img_url:
                m2=re.findall(self.pattern_img,str(item))
                img_m.append(m2[0])
            return img_m
        #with open('img_url.txt','w') as fimg:
            #fimg.write(str(img_m))

    def mkdir(self,path):
        path=str(path).strip()
        isExist=os.path.exists(path)
        if not isExist:
            os.makedirs(path)
            return True
        else:
            return False


    def dl_img(self,url_img,filepath=2015):
        self.mkdir(filepath)
        m=re.findall(self.pattern_dl,url_img)[0]
        file_n=str(2015)+'/'+m
        #print(m)
        #print(filename)
        with request.urlopen(url_img) as f:
            data=f.read()
            with open(file_n,'wb') as img:
                img.write(data)


    def parsePages(self,pageIndex):
        page_url=self.head_url+self.get_forum_url()+str(pageIndex)+'.html'
        #soup_tmp=self.url_parse(page_url)
        m_topic=self.url_parse_topic(page_url)
        for ts in m_topic:
            ts_url=self.head_url+str(ts)
            #print(ts_url)
            #if ts_url=='http://bbs.voc.com.cn/topic-1352942-1-1.html':
            #    pass
            #else:
            #soup_tmp2=self.url_parse(ts_url)
            m_img=self.url_parse_img(ts_url)
            print(m_img)
            for img in m_img:
                self.dl_img(img)


    def getPages(self,start,end):
        for i in range(start,end+1):
            self.parsePages(i)

if __name__=='__main__':
    spider=hs_spider()
    spider.set_forum_id(50)
    spider.getPages(2,3)
