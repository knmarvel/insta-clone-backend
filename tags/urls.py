from django.urls import path
from tags.views import tag_list

urlpatterns = [
    path("tag/<str:slug>/", tag_list, name="tag_list"),
]
