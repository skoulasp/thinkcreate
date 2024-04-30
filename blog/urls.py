from django.urls import path, include
from . import views
from .views import blog, post, search, cat_search, post_search, order_by, UpdateCommentVote	
from accounts.views import *

urlpatterns = [
    path('', blog, name='blog'),
    path('search/', search, name='search'),
    path('search/cat/', cat_search, name='search-cat'),
    path('search/posts/', post_search, name='search-posts'),
    path('order/', order_by, name='order'),
    path('<slug:slug>', post, name='post'),
    path('<slug:slug>/<int:comment_id>/<str:option>', views.UpdateCommentVote.as_view(), name='comment_likes'),
    path('api/<slug:slug>/<int:comment_id>/<str:option>', views.UpdateCommentVoteAPI.as_view(), name='comment_likes_api'),
]