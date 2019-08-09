# -*- coding: utf-8 -*-

from django.urls import path,re_path
from . import views,list_views


app_name = 'article'

urlpatterns = [
    path ('article-column/',views.article_column,name='article_column'),
    path ('rename-column/',views.rename_article_column,name='rename_article_column'),
    path ('del-column/',views.del_article_column,name='del_article_column'),
    path ('article-post/',views.article_post,name='article_post'),
    path ('article-list/',views.article_list,name='article_list'),
    path ('del-article/',views.del_article,name='del_article'),
    path ('redit-article/<int:article_id>/',views.redit_article,name='redit_article'),

    re_path('article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$',
            views.article_detail,name='article_detail'),

    path ('list-article-titles/',list_views.article_titles,name='article_titles'),  # 和下下个path调用同一个视图函数，但是path的name不一样

    path ('article-content/<int:id>/<slug:slug>/',list_views.article_detail,name='article_content'),

    path ('list-article-titles/<username>/',list_views.article_titles,name='author_articles'), # 这是下下个path

    path ('like-article/',list_views.like_article,name='like_article'),

]