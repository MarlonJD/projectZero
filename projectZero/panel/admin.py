from django.contrib import admin
from . import models

admin.site.register(models.Album)
admin.site.register(models.Artist)
admin.site.register(models.OtherArtist)
admin.site.register(models.Track)
admin.site.register(models.Partner)
