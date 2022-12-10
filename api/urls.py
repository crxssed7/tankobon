from django.urls import path

from .views import get_manga, get_specific_manga, get_manga_volumes

urlpatterns = [
    path("manga/", get_manga, name="get_manga"),
    path("manga/<int:manga_id>/", get_specific_manga, name="get_specific_manga"),
    path("manga/<int:manga_id>/volumes/", get_manga_volumes, name="get_manga_volumes"),
]
