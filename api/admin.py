from django.contrib import admin
from .models import Manga, Volume

# Register your models here.
admin.site.register(Manga)

@admin.register(Volume)
class VolumeAdmin(admin.ModelAdmin):
    list_filter = ('manga',) 