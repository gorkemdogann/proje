from django.urls import path
from .views import *

urlpatterns = [
    path('', posts_list, name='post-list'),
    path('post-create/', post_create, name='post-create'),
    path('post-detail/<slug:slug>/', post_detail, name='post-detail'),
    path('post-update/<slug:slug>/', post_update, name='post-update'),
    path('post-delete/<slug:slug>/', post_delete, name="post-delete"),
    path('add-comment/<slug:slug>/', add_comment, name="add-comment"),

]
