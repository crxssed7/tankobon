from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from api.models import Volume, Collection

class CollectionView(LoginRequiredMixin, View):
    def post(self, request, volume_id, *args, **kwargs):
        volume = get_object_or_404(Volume, pk=volume_id, absolute_number__gt=-1)
        if volume.has_collected(request.user):
            return JsonResponse({'message': 'Action unsuccessful'}, status=400)
        Collection.objects.create(volume=volume, user=request.user)
        if request.htmx:
            return HttpResponse('')
        return JsonResponse({'message': 'Action successful', 'type': 'collected'})

    def delete(self, request, volume_id, *args, **kwargs):
        volume = get_object_or_404(Volume, pk=volume_id, absolute_number__gt=-1)
        if not volume.has_collected(request.user):
            return JsonResponse({'message': 'Action unsuccessful'}, status=400)
        collection = Collection.objects.get(volume=volume, user=request.user)
        collection.delete()
        if request.htmx:
            return HttpResponse('')
        return JsonResponse({'message': 'Action successful', 'type': 'uncollected'})
