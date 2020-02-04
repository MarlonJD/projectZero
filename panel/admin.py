from django.contrib import admin
from . import models

admin.site.register(models.Album)
admin.site.register(models.Artist)
admin.site.register(models.OtherArtist)
admin.site.register(models.Track)
admin.site.register(models.Platform)
admin.site.register(models.ContentID)
admin.site.register(models.Statistic)
admin.site.register(models.Statement)
admin.site.register(models.RecordLabel)
admin.site.register(models.Genre)
admin.site.register(models.Announcement)
admin.site.register(models.SplitStatement)
