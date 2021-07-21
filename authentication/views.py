from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm

from django.template import loader
from django.http import HttpResponse
from django import template

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    
    if request.user.is_authenticated:
        if request.user.username == 'admin':
            return redirect("/dashadmin")
        else:
            return redirect("/dashtamu")
    else:
        if request.method == "POST":

            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                try:
                    user = authenticate(username=User.objects.get(email=username), password=password)
                except:  
                    user = authenticate(username=username, password=password)
    
                if user is not None:
                    login(request, user)
                    if user.username == 'admin':
                        return redirect("/dashadmin")
                    else:
                        return redirect("/dashtamu")
                else:    
                    msg = 'Invalid credentials'    
            else:
                msg = 'Error validating the form'    

        return render(request, "auth/login.html", {"form": form, "msg" : msg})


def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True
            
            return redirect("/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "auth/register.html", {"form": form, "msg" : msg, "success" : success })