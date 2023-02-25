from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.views.generic.detail import DetailView

from chartkick.django import PieChart, ColumnChart

from api.models import Volume, Collection
from tankobon.utils import get_user_image


class UserDetailView(DetailView):
    model = User
    template_name = "web/users/user_library.html"
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

    def get_template_names(self):
        if self.request.htmx:
            return ['web/users/_user_library.html']
        return ['web/users/user_library.html']


class UserStatisticsView(DetailView):
    model = User
    template_name = "web/users/user_statistics.html"
    slug_field = "username"
    context_object_name = "object"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context["object"]
        context["avatar"] = get_user_image(user.email)
        context["volume_count"] = user.collection_set.count()

        monthly_collected = (
            Collection.objects.filter(user=user).annotate(month=TruncMonth("created_at"))
                .values("month")
                .annotate(count=Count("month"))
                .order_by("-month")[:12]
        )
        monthly_collected_dict = {}
        for collected in reversed(monthly_collected):
            month_str = collected["month"].strftime("%b %Y")
            monthly_collected_dict[month_str] = collected["count"]
        context["monthly_collected"] = ColumnChart(monthly_collected_dict)

        # <QuerySet [{'manga__genres__name': 'Seinen', 'count': 3}, {'manga__genres__name': 'Shounen', 'count': 4}, {'manga__genres__name': 'Josei', 'count': 1}]>
        demograph_counts = Volume.objects.filter(collection__user=user, manga__genres__name__in=["Shounen", "Shoujo", "Seinen", "Josei"]).values('manga__genres__name').annotate(count=Count('id'))

        # Returns an array with one element e.g. [4]. The element is the count
        shounen_count = list(demograph_counts.filter(manga__genres__name='Shounen').values_list('count', flat=True))
        shoujo_count = list(demograph_counts.filter(manga__genres__name='Shoujo').values_list('count', flat=True))
        seinen_count = list(demograph_counts.filter(manga__genres__name='Seinen').values_list('count', flat=True))
        josei_count = list(demograph_counts.filter(manga__genres__name='Josei').values_list('count', flat=True))

        # Get that first element count
        shounen_count = shounen_count[0] if shounen_count else 0
        shoujo_count = shoujo_count[0] if shoujo_count else 0
        seinen_count = seinen_count[0] if seinen_count else 0
        josei_count = josei_count[0] if josei_count else 0

        context["demographs"] = PieChart({'Shounen': shounen_count, 'Shoujo': shoujo_count, 'Seinen': seinen_count, 'Josei': josei_count})
        return context

    def get_template_names(self):
        if self.request.htmx:
            return ['web/users/_user_statistics.html']
        return ['web/users/user_statistics.html']
