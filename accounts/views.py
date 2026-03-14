from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)
            return redirect("/customers/dashboard/")

    return render(request, "auth/login.html")

def register_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("/accounts/login")

    return render(request, "auth/register.html")

def logout_view(request):

    logout(request)

    return redirect("/accounts/login")