from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, LoginForm, AuthorAdminChangeForm
from .models import Author, Profile
from insta_backend.models import Post
from tags.models import Tag
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from insta_backend.helpers import notify_follow_helper


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
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('home')))
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):

    auth.logout(request)
    return redirect('login')


def profile_view(request, slug):

    user = Author.objects.get(slug=slug)
    profile = Profile.objects.filter(user=user).first()
    posts = Post.objects.filter(author=user)
    followers = Author.objects.filter(following=user)

    context = {
            "profile": profile,
            "posts": posts,
            "user": user,
            "followers": followers,
        }
    if request.user.is_authenticated:
        logged_in_user = Author.objects.get(id=request.user.id)
        is_following = logged_in_user.following.filter(slug=slug).exists()
        context["is_following"] = is_following
    return render(request, 'profile.html', context)


@login_required
def profile_edit_view(request, slug):
    user = Author.objects.get(slug=slug)
    profile = Profile.objects.filter(user=user).first()
    if request.method == 'POST':
        form = AuthorAdminChangeForm(
            request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
        return redirect('/user/'+user.slug)
    else:
        form = AuthorAdminChangeForm(instance=profile)
        context = {'form': form}
    return render(request, 'edit_profile.html', context)


def search_view(request):
    template = 'search.html'
    query = request.GET.get('q')
    author_results = Author.objects.filter(Q(username__icontains=query))
    tag_results = Tag.objects.filter(text__contains=query)
    context = {
        'author_results': author_results,
        'tag_results': tag_results
    }
    return render(request, template, context)


def follow_view(request, slug):
    user_follow = Author.objects.get(slug=slug)
    logged_in_user = Author.objects.get(username=request.user.username)
    logged_in_user.following.add(user_follow)
    notify_follow_helper(logged_in_user, user_follow, 'follow')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def unfollow_view(request, slug):
    user_unfollow = Author.objects.get(slug=slug)
    logged_in_user = Author.objects.get(id=request.user.id)
    logged_in_user.following.remove(user_unfollow)
    print(user_unfollow.username)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def all_users_view(request):
    template = 'all_users.html'
    users = Author.objects.all().order_by('username')
    context = {
        'users': users,
    }
    return render(request, template, context)
