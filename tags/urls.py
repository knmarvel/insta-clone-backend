from django.urls import path
from tags.views import tag_list, all_tags_view

urlpatterns = [
    path("tag/<str:slug>/", tag_list, name="tag_list"),
    path("tags", all_tags_view, name="all_tags")
]
