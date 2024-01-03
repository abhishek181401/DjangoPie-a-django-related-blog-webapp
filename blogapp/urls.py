from django.urls import path
from . import views

urlpatterns = [
    path('post/<slug>',views.post_page,name="post_page"),
    path('',views.index,name="index"),
    path('tag/<slug>',views.tag_page,name="tag_page"),
    path('author/<slug>',views.author_page,name="author_page"),
    path('search/',views.search_page,name="search_page"),
    path('about/',views.about_page,name="about_page"),
    path('accounts/register/',views.register_page,name="register_page"),
    path('bookmark_blog/<slug>',views.bookmark_blog,name="bookmark_blog"),
    path('like-blog/<slug>',views.like_blog,name="like_blog"),
    path('bookmarked-blogs/',views.bookmarked_blogs,name="bookmarked_blogs"),
    path('all-blogs/',views.all_blogs,name="all_blogs"),
    path('all-liked-blogs/',views.all_blogs,name="all_liked_blogs"),
    
]
