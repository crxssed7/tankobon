from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('manga/', views.SearchResultsView.as_view(), name='search'),
    path('manga/<int:manga_id>/', views.detail, name='manga'),
]