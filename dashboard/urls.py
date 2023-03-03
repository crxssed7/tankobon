from django.urls import path

from .views import LibraryView, CollectionDetailView

urlpatterns = [
    path("", LibraryView.as_view(), name="dashboard"),
    path("<pk>/", CollectionDetailView.as_view(), name="collection"),
]
