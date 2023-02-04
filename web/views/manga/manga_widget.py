import base64
import textwrap
import requests

from django.views.generic.detail import DetailView

from api.models import Manga

class MangaWidgetView(DetailView):
    template_name = "web/manga/manga_widget.svg"
    content_type = "image/svg+xml"
    context_object_name = "manga"
    model = Manga

    def get_context_data(self, **kwargs):
        context = super(MangaWidgetView, self).get_context_data(**kwargs)
        manga = context["manga"]
        title = manga.name
        number = 25
        start = 9.6585464
        # Wraps text so that it looks good in SVG
        wrapper = textwrap.TextWrapper(width=number)
        titles = wrapper.wrap(text=title)
        dic = []
        for i in range(len(titles)):
            _title = {}
            _title["value"] = titles[i]
            _title["step"] = start
            dic.append(_title)
            start += 7

        # Get base64 of image
        poster = ""
        if manga.poster_url:
            poster = "data:image/png;base64," + base64.b64encode(
                requests.get(manga.poster_url).content
            ).decode("utf-8")

        context.update({"titles": dic[:5], "poster": poster})
        return context
