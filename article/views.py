from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from .models import ArticleColumn,ArticlePost,ArticleTag
from .forms import ArticleColumnForm,ArticlePostForm,ArticleTagFrom
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# 增加栏目
@login_required(login_url='/account/login/')
@csrf_exempt                                     # 加装饰器也是解决遇到CSRF问题的一种方法
def article_column(request):
    if request.method == 'GET':
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm
        return render(request,'article/column/article_column.html',{'columns':columns,'column_form':column_form})

    if request.method == 'POST':
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id,column=column_name)
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user,column=column_name)
            return HttpResponse('1')


# 修改栏目名称
@login_required(login_url='/account/login')
@require_POST    # 只接受通过POST提交的数据
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


# 删除栏目
@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article_column(request):
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


# 文章发布
@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                return HttpResponse('1')
            except:
                return HttpResponse('2')
        else:
            return HttpResponse('3')
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        return render(request,'article/column/article_post.html',
                      {'article_post_form':article_post_form,
                       'article_columns':article_columns})


# 文章标题列表
@login_required(login_url='/account/login')
def article_list(request):
    article_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(article_list,5)                   # 每页显示5个文章
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger :
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request,'article/column/article_list.html',{'articles':articles,'page':current_page})


# 文章详情
@login_required(login_url='/account/login')
def article_detail(request,id,slug):
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    return render(request,'article/column/article_detail.html',{'article':article})


# 删除文章的提示
@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article(request):
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

# 修改文章内容
@login_required(login_url='/account/login')
@csrf_exempt
def redit_article(request,article_id):
    if request.method == 'GET':
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        this_article_form = ArticlePostForm(initial={'title':article.title})
        this_article_column = article.column
        return render(request,'article/column/redit_article.html',
                      {
                          'article':article,
                          'article_columns':article_columns,
                          'this_article_column':this_article_column,
                          'this_article_form':this_article_form
                      })
    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            return HttpResponse('1')
        except:
            return HttpResponse('2')

# 添加文章标签
@login_required(login_url='/account/login')
@csrf_exempt
def article_tag(request):
    if request.method == 'GET':
        article_tags = ArticleTag.objects.filter(author=request.user)
        article_tag_form = ArticleTagFrom()
        return render(request,'article/tag/tag_list.html',
                      {'article_tags':article_tags,
                       'article_tag_form':article_tag_form})

    if request.method == 'POST':
        tag_post_form =  ArticleTagFrom(data=request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag = tag_post_form.save(commit=False)
                new_tag.author = request.user
                new_tag.save()
                return HttpResponse('1')
            except:
                return HttpResponse('提交的数据不能存储')
        else:
            return HttpResponse('提交违法！！')

# 删除文章标签
@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article_tag(request):
    tag_id = require_POST['tag_id']
    try:
        tag = ArticleTag.objects.get(id=tag_id)
        tag.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('2')