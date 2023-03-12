from django.db.models import Count
from django.db.models.functions import TruncMonth

from api.models import Volume, Collection


class Statistics:
    def __init__(self, user):
        self.user = user

    def public(self) -> dict:
        volume_count = self.user.collection_set.count()

        monthly_collected = (
            Collection.objects.filter(user=self.user).annotate(month=TruncMonth("collected_at"))
                .values("month")
                .annotate(count=Count("month"))
                .order_by("-month")[:12]
        )
        monthly_collected_dict = {}
        for collected in reversed(monthly_collected):
            month_str = collected["month"].strftime("%b %Y")
            monthly_collected_dict[month_str] = collected["count"]

        # <QuerySet [{'manga__genres__name': 'Seinen', 'count': 3}, {'manga__genres__name': 'Shounen', 'count': 4}, {'manga__genres__name': 'Josei', 'count': 1}]>
        demograph_counts = Volume.objects.filter(collection__user=self.user, manga__genres__name__in=["Shounen", "Shoujo", "Seinen", "Josei"]).values('manga__genres__name').annotate(count=Count('id'))

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

        demographs = {'Shounen': shounen_count, 'Shoujo': shoujo_count, 'Seinen': seinen_count, 'Josei': josei_count}

        return {
            "volume_count": volume_count,
            "monthly_collected": monthly_collected_dict,
            "demographs": demographs
        }
