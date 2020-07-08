from django.urls import path
from .views import Homepage, post_detail

urlpatterns = [
    path('', Homepage.as_view(), name='home'),
    path("post/<int:id>/", post_detail, name="post_detail")

]
