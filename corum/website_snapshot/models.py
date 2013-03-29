from django.db import models
from core.models import User, Case, AbstractBase
from django.core.files import File
import threading
import hashlib
from website_snapshot.snapshot import WebsiteArchive


class SnapshotCase(AbstractBase):
    case = models.ForeignKey(Case)
    owner = models.ForeignKey(User)
    url = models.URLField()

    @property
    def snapshot_count(self):
        return self.snapshot_set.all().count()

    def take_snapshot(self):
        ss = Snapshot(snapshot_case=self)
        ss.snapshot.save(self.id + ".zip", File(WebsiteArchive(self.url).snapshot()))
        ss.set_checksum()
        ss.save()


class Snapshot(AbstractBase):
    """
    A snapshot of a website, a SnapshotCase can
    have multiple Snapshots, perhaps a future feature
    could be to schedule taking snapshots.
    """
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