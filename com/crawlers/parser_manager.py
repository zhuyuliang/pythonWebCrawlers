# coding:utf8
import re
from HTMLParser import HTMLParser

from bs4 import BeautifulSoup
import urlparse

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from selenium import webdriver

class ParserManager(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        # print "Encountered the beginning of a %s tag" % tag
        if tag == 'img' or tag == "script":
            for (variable, value) in attrs:
                if variable == "src" or variable == "href":
                    self.links.append(value)
        if tag == "link":
            dic = dict(attrs)
            if dic['rel'] == "stylesheet":
                self.links.append(dic['href'])

    def parse(self, page_url, html_cont):
            if page_url is None or html_cont is None:
                return
            # 如果不方便配置环境变量。就使用phantomjs的绝对路径也可以
            driver = webdriver.Chrome()
            driver.get(page_url)
            data = driver.page_source
            driver.quit()
            soup = BeautifulSoup(data,'html.parser',from_encoding='utf-8')
            new_data = self._get_new_data(data,page_url,soup)
            return new_data

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        #href="http://www.cnblogs.com/zhuyuliang/p/5218635.html"
        links = soup.find_all('a',href=re.compile(r'http://www.cnblogs.com/zhuyuliang/p/...'))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url,new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self,data, page_url, soup):
        res_data = {}
        res_data['url'] = page_url

        #<a id="cb_post_title_url" class="postTitle2" href="http://www.cnblogs.com/zhuyuliang/p/5218635.html">Android开发代码规范</a>
        title_node = soup.find('a',class_='postTitle2')
        res_data['title'] = title_node.get_text()

        #div id='topics'
        summary_node = soup.find('div',class_="post")
        res_data['summary'] = summary_node

        new_tag = soup.new_tag("body")
        new_tag.string = summary_node.encode('utf-8')
        soup.body.replace_with(new_tag)
        #print soup.encode('utf-8')
        res_data['template'] = soup

        res_data['data'] = data;

        return res_data

    def parseUrls(self,root_url,html_cont):
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(root_url, soup)
        return new_urls
