from django.shortcuts import render, reverse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.http import Http404
from django.template import RequestContext
from datetime import datetime as dt
from django.views import View
from insta_backend.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView


# Create your views here.
class Homepage(View):
    html = "index.html"

    def get(self, request):
        posts = None
        if request.user.is_authenticated:
            posts = Post.objects.filter(
                author__in=request.user.following.all())
        else:
            posts = Post.objects.all()
        posts = posts.order_by('-created_timestamp')
        return render(request, self.html, {'posts': posts})


def post_detail(request, id):
    html = "post_detail.html"
    try: 
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        raise Http404("That post doesn't exist :(")
    return render(request, html, {'post': post})


class PostAdd(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['image', 'caption']

    def form_valid(self, form):
        """Gives the user authorship of the new post"""
        form.instance.author = self.request.user
        form.instance.creation_timestamp = dt.now()
        return super().form_valid(form)

    def get_success_url(self):
        """Sends user back to homepage after post"""
        return reverse_lazy('home')


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post

    def check_ownership(self):
        """Checks to make sure the person requesting deletion
        owns the post"""
        post = super(PostDelete, self).get_object()
        if not post.author == self.request.user:
            raise Http404("You can't delete a post you don't own :( ")

    success_url = reverse_lazy('home')


def post_toggle_like(request, pk):
    try: 
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        raise Http404("You can't like a post that doesn't exist :(")
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    post.save()
    return HttpResponseRedirect(request.GET.get('next', reverse('home')))


def handler404(request, *args, **argv):
    responst = render(request, '404.html', {},
                      context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, '500.html', {},
                      context_instance=RequestContext(request))
    response.status_code = 500
    return response
