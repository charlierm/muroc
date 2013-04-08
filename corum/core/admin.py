from django.contrib.gis import admin
from models import *
from django.db import models


for model in models.get_models():
    try:
        admin.site.register(model, admin.OSMGeoAdmin)
    except Exception:
        continue
