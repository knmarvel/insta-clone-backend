from django.shortcuts import render
from django.views import View
from insta_backend.models import Post

# Create your views here.
class Homepage(View):
    html = "index.html"

    def get(self, request):
        print("posts view activated!!!")
        posts = None
        if request.user.is_authenticated:
            posts = Post.objects.filter(author__in=request.user.following.all())
        else:
            posts = Post.objects.all()
        
        return render(request, self.html, {'posts': posts})


def post_detail(request, id):
    html = "post_detail.html"
    post = Post.objects.get(id=id)
    return render(request, html, {'post': post})
