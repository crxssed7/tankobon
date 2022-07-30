from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contrib/', views.contrib, name='contrib'),
    path('docs/', views.docs, name='docs'),
    path('manga/', views.SearchResultsView.as_view(), name='search'),
    path('manga/<int:manga_id>/', views.detail, name='manga'),
    path('manga/new/', views.new_manga, name='new_manga'),
    path('manga/all/', views.all_manga, name='all_manga'),
    path('manga/<int:manga_id>/edit/', views.edit_manga, name='edit_manga'),
    path('manga/<int:manga_id>/edit/<int:volume_number>/', views.edit_volume, name='edit_volume'),
    path('manga/<int:manga_id>/edit/non/', views.edit_non_volume, name='edit_non_volume'),
    path('manga/<int:manga_id>/new/', views.new_volume, name='new_volume'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
]