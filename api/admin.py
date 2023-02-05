from simple_history.admin import SimpleHistoryAdmin

from django.contrib import admin

from .models import Manga, Volume, Edition, Genre, Language


@admin.action(description="Mark selected as locked")
def lock_records(modeladmin, request, queryset):
    queryset.update(locked=True)


@admin.action(description="Mark selected as unlocked")
def unlock_records(modeladmin, request, queryset):
    queryset.update(locked=False)


@admin.register(Edition)
class EditionAdmin(SimpleHistoryAdmin):
    list_display = ["manga", "name"]


@admin.register(Volume)
class VolumeAdmin(SimpleHistoryAdmin):
    list_display = ["manga", "absolute_number", "edition"]
    list_filter = ("manga",)
    actions = (lock_records, unlock_records)


@admin.register(Manga)
class MangaAdmin(SimpleHistoryAdmin):
    list_display = ["name", "last_updated"]
    actions = (lock_records, unlock_records)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name", "icon"]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]
