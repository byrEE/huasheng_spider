#!/usr/bin/env python3
# coding=utf-8
from urllib import request
from bs4 import BeautifulSoup
from get_ua import get_ua
import re
import os


class hs_spider(object):
    def __init__(self):
        self.head_url='http://bbs.voc.com.cn/'
        self.pattern_topic=re.compile(r'(topic-6.*?html)')
        self.pattern_dl=re.compile(r'.*?/\w/.*?/\d+/\d+/(\d+-\d+.jpg)')
        self.pattern_img=re.compile(r'http://image.hnol.net.*?jpg')
        self.cnt=0


    def set_forum_id(self,id=50):
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


    def url_parse_topic(self,url_topic):
        print('parsing url: '+url_topic)
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


    def url_parse_img(self,url):
        req=request.Request(url)
        print(url)
        req.add_header('user-agent',get_ua())
        with request.urlopen(req) as imgpage:
            data1=imgpage.read().decode('gbk')
            soup_img=BeautifulSoup(data1,'lxml')
            img_url=soup_img.find_all('a',href=self.pattern_img)
            print('This url included %s pictures' % len(img_url))
            img_m=[]
            for item in img_url:
                m2=re.findall(self.pattern_img,str(item))
                img_m.append(m2[0])
            return img_m


    def mkdir(self,path):
        path=str(path).strip()
        isExist=os.path.exists(path)
        if not isExist:
            os.makedirs(path)
            return True
        else:
            return False


    def dl_img(self,url_img,filepath=50):
        filepath=self.forum_id
        self.mkdir(filepath)
        m=re.findall(self.pattern_dl,url_img)[0]
        file_n=str(filepath)+'/'+m
        with request.urlopen(url_img) as f:
            data=f.read()
            with open(file_n,'wb') as img:
                img.write(data)
                self.cnt+=1


    def parsePages(self,pageIndex):
        if self.cnt%500==0:
            print('%s pictures has been downloaded' % self.cnt)
        page_url=self.head_url+self.get_forum_url()+str(pageIndex)+'.html'
        m_topic=self.url_parse_topic(page_url)
        for ts in m_topic:
            ts_url=self.head_url+str(ts)
            m_img=self.url_parse_img(ts_url)
            #print(m_img)
            for img in m_img:
                self.dl_img(img)


    def getPages(self,start,end):
        for i in range(start,end+1):
            self.parsePages(i)

if __name__=='__main__':
    spider=hs_spider()
    #fid=input('请输入要下载的板块id：')
    print('*****************************')
    print('''    辣眼 id: 76
    老照片 id: 57
    自拍 id: 22
    mn id:50
    摄影 id: 72
    户外 id: 17''')
    print('*****************************')
    fid=input('请输入要下载的板块id：')
    spider.set_forum_id(fid)
    startPage=int(input('请输入起始page : '))
    endPage=int(input('请输入结束page : '))
    spider.getPages(startPage,endPage)
