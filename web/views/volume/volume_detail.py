from django.views.generic.detail import DetailView

from api.models import Volume

class VolumeDetailView(DetailView):
    template_name = "web/volume/volume_detail.html"
    context_object_name = "volume"
    model = Volume

    def get_context_data(self, **kwargs):
        context = super(VolumeDetailView, self).get_context_data(**kwargs)
        volume = context["volume"]
        user = volume.history.exclude(history_user=None).values("history_user__username").first()
        last_edited_by = None
        if user:
            last_edited_by = user["history_user__username"]

        context.update({"manga": volume.manga, "last_edited_by": last_edited_by})
        return context

    def get_template_names(self):
        if self.request.htmx:
            return ['web/volume/_volume_detail.html']
        return ['web/volume/volume_detail.html']
