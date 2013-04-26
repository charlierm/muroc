from django.db import models
from core.models import User, Case, AbstractBase
import hashlib
from website_snapshot import tasks


class SnapshotCase(AbstractBase):
    case = models.ForeignKey(Case)
    owner = models.ForeignKey(User)
    url = models.URLField()

    @property
    def snapshot_count(self):
        return self.snapshot_set.all().count()

    def take_snapshot(self):
        tasks.take_snapshot.delay(self.pk)

    class Meta:
        permissions = [
            ("can_create", "User can create snapshots of websites"),
            ("can_delete", "User can delete existing snapshot cases"),
            ("can_read", "User can view website snapshot cases"),
            ("can_update", "User can edit existing snapshot cases")]


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

    class Meta:
        permissions = [
            ("can_create",
             "User can create snapshots of websites for existing case"),
            ("can_delete", "User can delete existing snapshots"),
            ("can_read", "User can view website snapshots")]
