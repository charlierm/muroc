from celery import task
from django.contrib.gis.geos import *
import exif_location


@task()
def get_exif(exifdata):
    from exif.models import ExifTag
    image = exifdata.image.file.name
    exif_data = exif_location.get_exif_data(image)

    for key, value in exif_data.iteritems():
        if key == 'GPSInfo':
            continue
        t = ExifTag(image=exifdata)
        t.key = str(key)
        t.value = str(value)
        t.save()

    location = exif_location.get_lat_lon(exif_data)
    if location:
        exifdata.location = Point(location[1], location[0])
        exifdata.save()
