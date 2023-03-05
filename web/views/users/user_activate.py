from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.http import HttpResponse, HttpResponseRedirect

from api.tokens import account_activation_token

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS, "Your account has sucessfully been activated.")
        return HttpResponseRedirect(reverse("login"))
    return HttpResponse('Activation link is invalid!')
