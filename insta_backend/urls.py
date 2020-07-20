from django.urls import path
from .views import (
    Homepage,
    post_detail,
    PostAdd,
    PostDelete,
    post_toggle_like,
    add_comment_to_post,
    comment_remove,
    comment_approve)

urlpatterns = [
    path('', Homepage.as_view(), name='home'),
    path("post/<int:id>/", post_detail, name="post_detail"),
    path('post/add/', PostAdd.as_view(), name="post-add"),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post-delete'),
    path('post/<int:pk>/like/', post_toggle_like, name='post-like'),
    path(
        'post/<int:pk>/add_comment_to_post/',
        add_comment_to_post,
        name='add_comment_to_post'
        ),
    path('comment/<int:pk>/approve/', comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', comment_remove, name='comment_remove'),
]
