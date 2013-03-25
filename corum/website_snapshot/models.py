from django.db import models
from core.models import User, Case, AbstractBase
from django.core.files import File
import urllib2
import zipfile
import tempfile
import urlparse
import threading
import hashlib
from BeautifulSoup import BeautifulSoup



class SnapshotCase(AbstractBase):
    case = models.ForeignKey(Case)
    owner = models.ForeignKey(User)
    url = models.URLField()

    @property
    def snapshot_count(self):
        return self.snapshot_set.all().count()

    def save(self, *args, **kwargs):
        if not self.snapshot_count:
            self.take_snapshot()
        super(SnapshotCase, self).save(*args, **kwargs)

    def take_snapshot(self):
        threading.Thread(target=self._take_snapshot).start()

    def _take_snapshot(self):
        tmp_zip = tempfile.NamedTemporaryFile()
        zp = zipfile.ZipFile(tmp_zip, 'w')
        files = []
        html = urllib2.urlopen(self.url)
        soup = BeautifulSoup(html)
        for image in soup.findAll(['img', 'script']):
            if not image.has_key('src'):
                continue
            url = urlparse.urljoin(self.url, image['src'])
            file_name = url.split('/')[-1]
            if len(file_name) > 240:
                file_name = file_name[-240:]
            temp = tempfile.NamedTemporaryFile()
            response = urllib2.urlopen(url)
            temp.write(response.read())
            files.append((temp, file_name))

        for f in files:
            zp.write(f[0].name, f[1])

        zp.close()
        snapshot = Snapshot(snapshot_case=self)
        with open(tmp_zip.name, 'rb') as snap_file:
            snapshot.snapshot.save(self.id + ".zip", File(snap_file))
        snapshot.save()
        snapshot.set_checksum()



class Snapshot(AbstractBase):
    date = models.DateTimeField(auto_now_add=True)
    snapshot = models.FileField(upload_to='site_snapshot')
    snapshot_case = models.ForeignKey(SnapshotCase)
    snapshot_hash = models.CharField(max_length=64, editable=False)

    def set_checksum(self, blocksize=65536):
        hasher = hashlib.sha256()
        snap = self.snapshot.file
        buf = snap.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = snap.read(blocksize)
        print hasher.hexdigest()

