from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import Http404
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
        posts.order_by('timestamp')
        return render(request, self.html, {'posts': posts})


def post_detail(request, id):
    html = "post_detail.html"
    post = Post.objects.get(id=id)
    return render(request, html, {'post': post})


class PostAdd(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['image', 'caption']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post

    def check_ownership(self):
        """Checks to make sure the person requesting deletion
        owns the post"""
        post = super(PostDelete, self).get_object()
        if not post.author == self.request.user:
            raise Http404

    success_url = reverse_lazy('home')
