from django.contrib.auth.views import LogoutView, PasswordChangeView,PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, register_converter
from django.views.generic import TemplateView

from web.converters import NegativeIntConverter

from web.views.edition.edition_new import new_edition

from web.views.manga.manga_detail import MangaDetailView
from web.views.manga.manga_edit import edit_manga
from web.views.manga.manga_list import ListMangaView
from web.views.manga.manga_new import new_manga
from web.views.manga.manga_search import SearchResultsView
from web.views.manga.manga_widget import MangaWidgetView

from web.views.singles.views import (
    IndexView,
    HelpNeededView,
)
from web.views.users.user_detail import UserDetailView, UserStatisticsView
from web.views.users.user_login import login_view
from web.views.users.user_signup import SignUpView
from web.views.users.user_activate import activate

from web.views.volume.volume_collect import CollectionView
from web.views.volume.volume_detail import VolumeDetailView
from web.views.volume.volume_edit import edit_volume
from web.views.volume.volume_new import new_volume

register_converter(NegativeIntConverter, "negint")

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("guidelines/", TemplateView.as_view(template_name="web/contrib.html"), name="contrib"),
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

    path("volume/<pk>", VolumeDetailView.as_view(), name="volume"),

    path("edition/new/", new_edition, name="new_edition"),

    path("collect/<int:volume_id>/", CollectionView.as_view(), name="collect"),

    path("accounts/login/", login_view, name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("accounts/activate/<uidb64>/<token>/", activate, name="activate"),
    path("accounts/password_change/", PasswordChangeView.as_view(), name="password_change"),
    path("accounts/password_change/done/", PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("accounts/password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("accounts/password_reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("accounts/reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("accounts/reset/done/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path("users/<slug>/", UserDetailView.as_view(), name="user"),
    path("users/<slug>/stats/", UserStatisticsView.as_view(), name="public_user_stats"),
]
