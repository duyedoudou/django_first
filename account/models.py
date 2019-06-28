from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    birth = models.DateField(blank=True,null=True)
    phone = models.CharField(max_length=20,null=True)

# 创建个人信息相关的数据模型类
class UserInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    school = models.CharField(max_length=100,blank=True)
    company = models.CharField(max_length=100,blank=True)
    profession = models.CharField(max_length=100,blank=True)   # 职业
    address = models.CharField(max_length=100,blank=True)
    aboutme = models.TextField(blank=True)
    photo = models.ImageField(blank=True)


    def __str__(self):
        return 'user {}'.format(self.user.username)

