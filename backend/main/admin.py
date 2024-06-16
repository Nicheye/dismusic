from django.contrib import admin
from main.models import Album, Track, Like, DisLike

admin.site.register(Album)
admin.site.register(Track)
admin.site.register(Like)
admin.site.register(DisLike)
