from django.db.models.signals import post_save
from django.dispatch import receiver
from exif.models import ExifData


@receiver(post_save, sender=ExifData)
def get_exif(sender, instance, created, **kwargs):
    if created:
        instance.get_exif()
