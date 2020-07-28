from django.urls import path
from django.conf.urls import url
from .views import post_list,post_detail,post_new,post_edit,post_share
from .feeds import LatestPostsFeed

urlpatterns = [
    path('',post_list,name='post_list'),
    #path('post/<int:pk>/',post_detail, name='post_detail'),
    path('post/new/', post_new, name='post_new'),
    path('post/<int:pk>/edit/', post_edit, name='post_edit'),
    path('post/<int:pk>/share/',post_share,
    name='post_share'),

    path('post/<int:pk>/',post_detail, name='post_detail'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', post_list,
     name='post_list_by_tag'),
    url(r'^feed/$', LatestPostsFeed(), name='post_feed')
]