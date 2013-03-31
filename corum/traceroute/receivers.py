from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from models import TracerouteCase



@receiver(post_save, sender=TracerouteCase)
def start_traceroute(sender, instance, created, **kwargs):
    if created:
        instance.start_traceroute()