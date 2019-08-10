# -*- coding: utf-8 -*-
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

import markdown

from article.models import ArticlePost


register = template.Library()

# 统计总共文章数量
@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()

# 统计个人文章数量
@register.simple_tag
def author_total_articles(user):
    return user.article.count()

# 展示最新文章
@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by('-created')[:n]
    return {'latest_articles':latest_articles}

# 展示评论最多的文章
@register.simple_tag
def most_commented_articles(n=3):
    return ArticlePost.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:n]

# markdown转成html编码
@register.filter(name='markdown')
def markdown_filter(text):
    return mark_safe(markdown.markdown(text))