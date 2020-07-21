from django.urls import path
from .views import (
    notification_view
)

urlpatterns = [
    path('notifications/', notification_view, name='notifications')
]