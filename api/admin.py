from django.contrib import admin
from .models import Manga, Chapter

# Register your models here.
admin.site.register(Manga)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_filter = ('manga',)