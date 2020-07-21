from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    reverse,
    HttpResponseRedirect,
    redirect,
    get_object_or_404
)
from django.urls import reverse_lazy
from django.http import Http404
from django.template import RequestContext
from datetime import datetime as dt
from django.views import View


from comments.forms import CommentForm
from comments.models import Comments
from insta_backend.models import Post
from insta_backend.helpers import check_for_tags

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from notification.models import Notification
from authentication.models import Author
import re
from .helpers import notify_helper
# Create your views here.
class Homepage(View):
    html = "index.html"

    def get(self, request):
        posts = None
        if request.user.is_authenticated and not request.GET.dict():
            posts = Post.objects.filter(
                author__in=request.user.following.all())
        else:
            posts = Post.objects.all()
        posts = posts.order_by('-created_timestamp')
        return render(request, self.html, {'posts': posts})


# def notification_alert(post):
#     mention_pattern = r'\B#\w*[a-zA-Z]+\w*'
#     tag = re.match(mention_pattern, post)
#     if tag:
#         tagged_user = Author.objects.get(username=username)
#         Notification.objects.create(
#             creator=request.user,
#             to=tagged_user,
#             post=post
#         )

def post_detail(request, id):
    html = "post_detail.html"
    post = Post.objects.get(id=id)
    comments = Comments.objects.filter(posts=post)
    return render(request, html, {'post': post, 'comments': comments})


class PostAdd(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['image', 'caption']

    def form_valid(self, form):
        """Gives the user authorship of the new post,
        checks for timestamp and tags"""
        form.instance.author = self.request.user
        form.instance.creation_timestamp = dt.now()
        created_request = super().form_valid(form)
        new_post = self.object
        # breakpoint()
        new_post.caption = check_for_tags(new_post.caption, new_post.id)
        
        new_post.save()
        
        return created_request

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
        notify_helper(request.user, post, 'like')
        
    post.save()
    return HttpResponseRedirect(request.GET.get('next', reverse('home')))


def handler404(request, *args, **argv):
    response = render(request, '404.html', {},
                      context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, '500.html', {},
                      context_instance=RequestContext(request))
    response.status_code = 500
    return response


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save()
            comment.post = post
            comment.save()
            new_comment = Comments.objects.create(
                posts=Post.objects.get(id=pk),
                author=request.user,
                text=comment.text)
            notify_helper(request.user, post, 'commente')
            print(new_comment)
            return HttpResponseRedirect(request.GET.get('next',
                                                        reverse('home')))
    else:
        form = CommentForm()
    return render(request, "add_comment_to_post.html", {'form': form})


@login_required
def comment_approve(request, pk):
    comments = get_object_or_404(Comments, pk=pk)
    comments.approve()
    return redirect('post_detail', pk=comments.post.pk)


@login_required
def comment_remove(request, pk):
    comments = get_object_or_404(Comments, pk=pk)
    comments.delete()
    return redirect('post_detail.html', pk=comments.post.pk)

