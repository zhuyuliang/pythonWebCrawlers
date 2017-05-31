# coding:utf8
import urllib2


class DownloadManager(object):

    def download(self, url):
        if url is None:
            return None
        response = urllib2.urlopen(url)
        if response.code != 200:
            return None
        return response.read()
