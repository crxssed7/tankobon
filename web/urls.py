from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from web.views.singles.views import contrib, docs, changelog, IndexView, HelpNeededView, SearchResultsView, SignUpView
from web.views.manga.views import detail, edit_manga, new_manga, widget, all_manga, all_manga_completed, all_manga_releasing
from web.views.volume.views import edit_non_volume, edit_volume, new_volume

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('guidelines/', contrib, name='contrib'),
    path('docs/', docs, name='docs'),
    path('changelog/', changelog, name='changelog'),
    path('help/', HelpNeededView.as_view(), name='help_needed'),

    path('manga/', SearchResultsView.as_view(), name='search'),
    path('manga/new/', new_manga, name='new_manga'),
    path('manga/all/', all_manga, name='all_manga'),
    path('manga/all/completed/', all_manga_completed, name='all_manga_completed'),
    path('manga/all/releasing/', all_manga_releasing, name='all_manga_releasing'),
    path('manga/<int:manga_id>/', detail, name='manga'),
    path('manga/<int:manga_id>/widget/', widget, name='widget'),
    path('manga/<int:manga_id>/edit/', edit_manga, name='edit_manga'),
    path('manga/<int:manga_id>/edit/<int:volume_number>/', edit_volume, name='edit_volume'),
    path('manga/<int:manga_id>/edit/non/', edit_non_volume, name='edit_non_volume'),
    path('manga/<int:manga_id>/new/', new_volume, name='new_volume'),

    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
]