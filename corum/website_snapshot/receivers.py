from website_snapshot.models import *
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


#TODO: Should be using a queue as opposed to a thread. Need to do some research
#      to establish which is best. This would be useful all over the project.
@receiver(post_save, sender=SnapshotCase)
def take_snapshot(sender, instance, created, **kwargs):
        if created:
            instance.take_snapshot()


@receiver(post_delete, sender=SnapshotCase)
def delete_snapshot_case(sender, instance, using, **kwargs):
    for ss in instance.snapshot_set.all():
        ss.snapshot.delete(False)


@receiver(post_delete, sender=Snapshot)
def delete_snapshot(sender, instance, using, **kwargs):
    instance.snapshot.delete(False)
