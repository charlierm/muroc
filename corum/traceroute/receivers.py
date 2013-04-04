from django.db.models.signals import post_save
from django.dispatch import receiver
from traceroute.models import TracerouteCase


@receiver(post_save, sender=TracerouteCase)
def start_traceroute(sender, instance, created, **kwargs):
    if created:
        instance.start_traceroute()
