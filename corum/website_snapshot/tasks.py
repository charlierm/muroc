from celery import task
from website_snapshot.wget import Wget
from django.core.files import File


@task()
def take_snapshot(snapshot_case):
    from website_snapshot.models import Snapshot
    ss = Snapshot(snapshot_case=snapshot_case)
    f = File(Wget(snapshot_case.url).start())
    ss.snapshot.save(snapshot_case.id + ".zip", f)
    ss.set_checksum()
    ss.save()
    return ss
