from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from django.urls import reverse
from slugify import slugify

# 栏目
class ArticleColumn(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='article_column')
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.column


# 文章标签的数据模型
class ArticleTag(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tag')
    tag = models.CharField(max_length=500)

    def __str__(self):
        return self.tag


# 文章的数据模型对象
class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, on_delete=models.CASCADE, related_name='article_column')
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    # 新增关于点赞
    users_like = models.ManyToManyField(User,related_name='articles_like',blank=True)
    # 新增关于标签
    article_tag = models.ManyToManyField(ArticleTag,related_name='article_tag',blank=True)


    class Meta:
        ordering = ('-updated',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(ArticlePost,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("article:article_detail",args=[self.id,self.slug])

    def get_url_path(self):
        return reverse('article:article_content',args=[self.id,self.slug])



# 文章的评论模型
class Comment(models.Model):
    article = models.ForeignKey(ArticlePost,on_delete=models.CASCADE,related_name='comments')
    body = models.TextField()
    commentator = models.CharField(max_length=90)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator.username,self.article)
        # return "Comment byon {1}".format(self.article)

