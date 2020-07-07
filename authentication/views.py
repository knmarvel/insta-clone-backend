from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from .models import Author
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(password=password)
            user.save()

    form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('/'))
    form = LoginForm()
    return render(request, 'login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('/login')


