from django.views.generic.detail import DetailView
from django.contrib.auth.models import User

from tankobon.utils import get_user_image


class UserDetailView(DetailView):
    model = User
    template_name = "web/user.html"
    slug_field = "username"
    context_object_name = "object"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["avatar"] = get_user_image(context["object"].email)
        return context
