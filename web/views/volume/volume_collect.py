from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, reverse
from django.views import View

from api.models import Volume, Collection

class CollectionView(LoginRequiredMixin, View):
    def post(self, request, volume_id, *args, **kwargs):
        volume = get_object_or_404(Volume, pk=volume_id, absolute_number__gt=-1)
        if volume.has_collected(request.user):
            return JsonResponse({'message': 'Action unsuccessful'}, status=400)
        collection = Collection.objects.create(volume=volume, user=request.user)
        if request.htmx:
            response = HttpResponse()
            response["HX-Redirect"] = reverse("collection", args=[collection.id])
            return response
        return JsonResponse({'message': 'Action successful', 'type': 'collected'})

    def delete(self, request, volume_id, *args, **kwargs):
        volume = get_object_or_404(Volume, pk=volume_id, absolute_number__gt=-1)
        if not volume.has_collected(request.user):
            return JsonResponse({'message': 'Action unsuccessful'}, status=400)
        collection = get_object_or_404(Collection, volume=volume, user=request.user)
        collection.delete()
        if request.htmx:
            messages.add_message(request, messages.ERROR, 'Volume was deleted from your collection.')
            response = HttpResponse()
            response["HX-Redirect"] = reverse("dashboard")
            return response
        return JsonResponse({'message': 'Action successful', 'type': 'uncollected'})
