from django.urls import path
from .views import (
    login_view, register_view, logout_view, profile_view, profile_edit_view, search_view, follow_view, unfollow_view
)

urlpatterns = [
    path('user/<str:slug>/edit_profile/', profile_edit_view, name='edit_profile'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('search/', search_view, name='search'),
    path('user/<str:slug>/', profile_view, name='profile'),
    path('follow/<str:slug>/', follow_view, name='follow'),
    path('unfollow/<str:slug>/', unfollow_view, name='unfollow'),
    path('register/', register_view, name='register')
]
