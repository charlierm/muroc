import urllib2
import re
import urlparse
import tempfile
import os
import pdb
import zipfile
from BeautifulSoup import BeautifulSoup

class WebsiteArchive(object):
    """Snapshot class for taking website forensic snapshots"""

    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17"
    opener = None
    html = None
    soup = None
    url = None
    _files = []

    def __init__(self, url):
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-agent', self.USER_AGENT)]
        self.html = self.opener.open(url).read()
        self.soup = BeautifulSoup(self.html)
        self.url = url

    def get_file(self, url):
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.write(self.opener.open(url).read())
        tmp.flush()
        os.fsync(tmp.fileno())
        return file(tmp.name, 'rb')

    def _images(self):
        imgs = []
        for img in self.soup.findAll("img"):
            if not img.has_key('src'):
                continue
            url = urlparse.urljoin(self.url, img['src'])
            imgs.append(url)
        return imgs

    def _scripts(self):
        scripts = []
        for script in self.soup.findAll("scripts"):
            if not script.has_key('src'):
                continue
            url = urlparse.urljoin(self.url, script['src'])
            scripts.append(url)
        return scripts

    @staticmethod
    def get_filename(url):
        file_name = url.split('/')[-1]
        if len(file_name) > 100:
            file_name = file_name[:100]
        return file_name

    def snapshot(self):
        tmp = tempfile.NamedTemporaryFile()
        zp = zipfile.ZipFile(tmp, 'w')
        for resource in self._images() + self._scripts():
            f = self.get_file(resource)
            self._files.append(f.name)
            name = self.__class__.get_filename(resource)
            zp.write(f.name, name)
            f.close()
        zp.write(self.get_file(self.url).name, 'index.html')
        zp.close()
        return file(tmp.name, 'rb')

    def __del__(self):
        for f in self._files:
            os.unlink(f)
