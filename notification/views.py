from django.shortcuts import render
from .models import Notification
from authentication.models import Author
from insta_backend.models import Post

def notification_view(request):
    notifications = Notification.objects.filter(to=request.user).order_by('-created_timestamp')
    user = Author.objects.get(username=request.user.username)
    
    posts = Post.objects.filter(author=user).order_by('-created_timestamp')
    return render(request, 'notifications.html', {
        'notifications': notifications,
        'posts': posts,
        
    })
