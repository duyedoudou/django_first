
# Register your models here.

from django.contrib import admin
from .models import BlogArticles

class BlogArticlesAdmin(admin.ModelAdmin):
    list_display = ("title","author","publish")   # Blog › Blog articless的展示列
    list_filter = ("publish","author")            # 右边栏过滤器
    search_fields = ("title","body")              # 搜索栏中的搜索范围
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ['-publish','author']

admin.site.register(BlogArticles,BlogArticlesAdmin)  # 注册到admin
