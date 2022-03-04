from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Task)
admin.site.register(models.SpaceList)
admin.site.register(models.SpaceFeature)
admin.site.register(models.SpaceFeatureList)