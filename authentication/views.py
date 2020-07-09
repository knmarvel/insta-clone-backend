from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, ProfileEditForm, AuthorAdminChangeForm
from .models import Author, Profile
from insta_backend.models import Post
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required




def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = Author.objects.create_user(
                username=form.cleaned_data['username'],
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            user.is_Active = True
            user.following.add(user)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse('home')))
    form = LoginForm()
    return render(request, 'login.html', {'form': form})
def logout_view(request):
    
    auth.logout(request)
    return redirect('login')

def profile_view(request, slug):
    
    user = Author.objects.get(username=slug)
    profile = Profile.objects.get(user=user)
    print(profile)
    print(user)
    
    
    posts = Post.objects.filter(author=user)
    
    context = {
            "profile": profile,
            "posts":posts,
            "user": user
        }
    return render(request, 'profile.html', context)

@login_required
def profile_edit_view(request, slug):
    user = Author.objects.get(username=slug)
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = AuthorAdminChangeForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            print("the form should be saving now")
        return redirect('/')
    else:
        form = AuthorAdminChangeForm(instance=profile)
        context = {'form': form }
    return render(request, 'edit_profile.html', context)