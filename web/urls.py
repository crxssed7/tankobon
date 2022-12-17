from django.urls import path, register_converter
from django.contrib.auth.views import LoginView, LogoutView

from web.converters import NegativeIntConverter
from web.views.manga.views import (
    edit_manga,
    new_manga,
    new_edition,
    MangaDetailView,
    MangaWidgetView,
    ListMangaView,
)
from web.views.singles.views import (
    IndexView,
    HelpNeededView,
    SearchResultsView,
    SignUpView,
    GuidelinesView,
    DocsView,
)
from web.views.users.views import UserDetailView
from web.views.volume.views import edit_volume, new_volume

register_converter(NegativeIntConverter, "negint")

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("guidelines/", GuidelinesView.as_view(), name="contrib"),
    path("docs/", DocsView.as_view(), name="docs"),
    path("help/", HelpNeededView.as_view(), name="help_needed"),
    path("manga/", SearchResultsView.as_view(), name="search"),
    path("manga/new/", new_manga, name="new_manga"),
    path("manga/all/", ListMangaView.as_view(), name="all_manga"),
    path("manga/<pk>/", MangaDetailView.as_view(), name="manga"),
    path("manga/<pk>/widget/", MangaWidgetView.as_view(), name="widget"),
    path("manga/<int:manga_id>/edit/", edit_manga, name="edit_manga"),
    path(
        "manga/<int:manga_id>/edit/<int:volume_number>/",
        edit_volume,
        name="edit_volume",
    ),
    path(
        "manga/<int:manga_id>/edit/<negint:volume_number>/",
        edit_volume,
        name="edit_volume",
    ),
    path("manga/<int:manga_id>/new/", new_volume, name="new_volume"),
    path("edition/new/", new_edition, name="new_edition"),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("users/<slug>/", UserDetailView.as_view(), name="user"),
]
