from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.db.models import Prefetch, Subquery

from api.models import Volume, Edition, Collection, Manga
from tankobon.utils import get_user_image


class UserDetailView(DetailView):
    model = User
    template_name = "web/users/user_detail.html"
    slug_field = "username"
    context_object_name = "object"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context["object"]
        context["avatar"] = get_user_image(user.email)
        collected_volumes = Volume.objects.prefetch_related("edition", "collection_set", "manga").filter(collection__user=user).order_by("edition__manga__name", "absolute_number")

        edition_volumes = {}
        for volume in collected_volumes:
            edition_name = f"{volume.manga} {volume.edition.name} Edition".title()
            if edition_name not in edition_volumes:
                edition_volumes[edition_name] = {'manga': volume.manga, 'volume_list': []}
            edition_volumes[edition_name]['volume_list'].append(volume)
        context["edition_volumes"] = edition_volumes
        return context
