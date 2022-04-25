from django.contrib import admin
from .models import Manga, Volume

# Register your models here.
@admin.action(description='Mark selected as locked')
def lock_records(modeladmin, request, queryset):
    queryset.update(locked=True)

@admin.action(description='Mark selected as unlocked')
def unlock_records(modeladmin, request, queryset):
    queryset.update(locked=False)

@admin.register(Volume)
class VolumeAdmin(admin.ModelAdmin):
    list_filter = ('manga',)
    actions = (lock_records, unlock_records)

@admin.register(Manga)
class VolumeAdmin(admin.ModelAdmin):
    actions = (lock_records, unlock_records)