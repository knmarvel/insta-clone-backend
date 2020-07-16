from django.shortcuts import render
from tags.models import Tag


# Create your views here.
def tag_list(request, slug):
    html = "tag_list.html"
    tag = Tag.objects.get(slug=slug)
    posts = tag.post.all()
    return render(request, html, {'posts': posts})
