# -*- coding:utf-8 -*-
# !/bin/sh
from bs4 import BeautifulSoup
import urllib2,os
import urllib

from lxml.html import html_parser, HTMLParser

from selenium import webdriver

from com.crawlers.parser_manager import ParserManager


class OutputManager(object):

    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)


    def output_html(self):
        for data in self.datas:
            fout = open('output/%s.txt'%data['title'].encode('utf-8'), 'w')
            fout.write("%s" % data['summary'].encode('utf-8'))
            fout.close()
            url = data['url'].encode('utf-8')
            pagename = data['title'].encode('utf-8')
            # html_code = urllib.urlopen(url).read()
            hp = ParserManager()
            html_code = data['template'].encode('utf-8')
            html_code = hp.unescape(html_code)
            data = data['data'].encode('utf-8')
            hp.feed(data)
            hp.close()
            durl = url.rsplit('/',1)[0]
            self.download(pagename,data,durl,hp.links)


    def download(self,pagename,html_code,durl,links):
        if not os.path.exists('output/'+pagename+'_files'):
            os.mkdir('output/'+pagename+'_files')
            upurl = durl.rsplit('/',1)[0]
            for link in links:
                fname = link.split('/')[-1]
                fname = fname.split('?')[0]
                localpath = '%s%s' % ('output/'+pagename+'_files/',fname)
                replacelocalpath = '%s%s' % (pagename + '_files/', fname)
                # if link[0:3] == '../':
                #         downlink = "http:" + link
                # else:
                #         downlink = link
                try:
                    if link[0:7] == 'http://':
                        urllib.urlretrieve(link,localpath)
                    else:
                        urllib.urlretrieve("http://www.cnblogs.com" + link,localpath)
                except Exception,error:
                    print 'download error:', error
                else:
                    print 'download '+fname
                    html_code = html_code.replace(link,replacelocalpath)
                open('output/'+pagename+'.html','w').write(html_code)
        return True

