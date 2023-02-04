from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse

from web.forms import LoginForm

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("search"))
        else:
            messages.error(request, "Username or password not correct")
            return redirect(reverse("login"))
    else:
        form = LoginForm()
    rendered_form = form.render("web/form_snippet.html")
    return render(request, "registration/login.html", {"form": rendered_form})
