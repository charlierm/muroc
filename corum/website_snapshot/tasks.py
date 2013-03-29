from celery import task
from website_snapshot.snapshot import WebsiteArchive
from django.core.files import File


@task()
def take_snapshot(snapshot_case):
    from website_snapshot.models import Snapshot
    ss = Snapshot(snapshot_case=snapshot_case)
    ss.snapshot.save(snapshot_case.id + ".zip", File(WebsiteArchive(snapshot_case.url).snapshot()))
    ss.set_checksum()
    ss.save()
    return ss
