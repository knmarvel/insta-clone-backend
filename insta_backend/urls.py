from django.urls import path
from .views import Homepage, post_detail, PostAdd, PostDelete, post_toggle_like

urlpatterns = [
    path('', Homepage.as_view(), name='home'),
    path("post/<int:id>/", post_detail, name="post_detail"),
    path('post/add/', PostAdd.as_view(), name="post-add"),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post-delete'),
    path('post/<int:pk>/like/', post_toggle_like, name='post-like')

]
