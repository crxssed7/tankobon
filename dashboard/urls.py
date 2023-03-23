from django.urls import path

from .views import LibraryView, CollectionDetailView, StatisticsView

urlpatterns = [
    path("", LibraryView.as_view(), name="dashboard"),
    path("stats/", StatisticsView.as_view(), name="private_stats"),
    path("<pk>/", CollectionDetailView.as_view(), name="collection"),
]
