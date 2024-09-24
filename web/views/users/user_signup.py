from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import redirect

from web.forms import SignUpForm

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        response = super().form_valid(form)
        if form.is_valid():
            messages.success(self.request, 'Your account has been created successfully. Please check your email to activate your account.')
        return response

def sign_up_view(request):
    return redirect("/")
