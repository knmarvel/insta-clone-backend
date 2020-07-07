from django.contrib import admin
from django.urls import path, include
from .views import (
<<<<<<< HEAD
    login_view, index, register_view, logout_view, profile_view
=======
    login_view, register_view, logout_view
>>>>>>> cabb80c9017b007778db0f6ae4d272aae8edcd7b
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user/<int:id>', profile_view, name='profile'),
    path('register/', register_view, name='register')
]
