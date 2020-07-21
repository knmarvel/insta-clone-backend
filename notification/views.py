from django.shortcuts import render
from .models import Notification
from authentication.models import Author

def notification_view(request):
    notifications = list(Notification.objects.filter(to=request.user))
    users = Author.objects.all()
    return render(request, 'notifications.html', {
        'notifications': notifications
    })