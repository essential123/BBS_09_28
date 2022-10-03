from django.shortcuts import render, HttpResponse, redirect
from .blog_forms import RegisterForm
from django.http import JsonResponse
from .models import User, BlogArticle, UserBlog, BlogTag, BlogCategory, BlogUpAndDown, BlogComment, Banner

from django.contrib.auth import authenticate
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import random
from django.contrib.auth.decorators import login_required
import json
from django.db.models import F
from django.db import transaction
from bs4 import BeautifulSoup


# Create your views here.
def register(request):
    if request.method == 'GET':
        register_form = RegisterForm()
        return render(request, 'register.html', context={'form': register_form})
    else:
        res = {'code': 100, 'msg': '注册成功'}
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            register_data = register_form.cleaned_data
            register_data.pop('re_password')
            picture = request.FILES.get('my_file')
            if picture:
                register_data['head'] = picture
            User.objects.create_user(**register_data)
            return JsonResponse(res)
        else:
            res['code'] = 101
            res['msg'] = '注册失败'
            res['errors'] = register_form.errors
            return JsonResponse(res)


def check_username(request):
    res = {'code': 100, 'msg': '用户已存在'}
    username = request.GET.get('username')
    user = User.objects.filter(username=username).first()
    if user:
        return JsonResponse(res)
    else:
        res['code'] = 101
        res['msg'] = '用户不存在'
        return JsonResponse(res)


def get_background_rgb():
    return (random.randint(0, 99), random.randint(0, 99), random.randint(0, 99))


def get_rgb():
    return (random.randint(99, 255), random.randint(99, 255), random.randint(99, 255))


def get_code(request):
    img = Image.new('RGB', (300, 35), get_background_rgb())
    font = ImageFont.truetype('./static/font/ss.TTF', 30)
    img_draw = ImageDraw.Draw(img)
    code_str = ''
    for i in range(5):
        number = random.randint(0, 9)
        capital_letter = chr(random.randint(65, 90))
        small_letter = chr(random.randint(97, 122))
        ran = str(random.choice([number, capital_letter, small_letter]))
        img_draw.text((40 + 50 * i, 0), ran, fill=get_rgb(), font=font)
        code_str += ran
    print(code_str)
    request.session['code'] = code_str
    width = 450
    height = 30
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)

        img_draw.line((x1, y1, x2, y2), fill=get_rgb())

    for i in range(1000):
        # 画点
        img_draw.point([random.randint(0, width), random.randint(0, height)], fill=get_rgb())
    byte_io = BytesIO()
    img.save(byte_io, 'png')

    return HttpResponse(byte_io.getvalue())


from django.contrib.auth import login as auth_login


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        res = {'code': 100, 'msg': '登录成功'}
        print(request.POST)
        real_code = request.session.get('code')
        code = request.POST.get('code')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if code.lower() == real_code.lower():
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                return JsonResponse(res)
            else:
                res['code'] = 101
                res['msg'] = '用户名或者密码错误'
                return JsonResponse(res)
        else:
            res['code'] = 102
            res['msg'] = '验证码错误'
            return JsonResponse(res)


def index(request):
    article_list = BlogArticle.objects.all()
    banner_list = Banner.objects.all()
    return render(request, 'index.html', context={'article_list': article_list, 'banner_list': banner_list})


def site(request, name, **kwargs):
    user = User.objects.filter(username=name).first()
    if user:
        article_list = BlogArticle.objects.all()
        type_name = kwargs.get('type_name')
        condition = kwargs.get('condition')
        if type_name == 'tag':
            article_list = article_list.filter(blog_tag__id=condition)
        elif type_name == 'category':
            article_list = article_list.filter(blog_category_id=condition)
        elif type_name == 'archive':
            year = str(condition)[:4]
            month = str(condition)[4:]
            article_list = article_list.filter(create_time__year=year, create_time__month=month)
        return render(request, 'site.html', locals())
    else:
        return render(request, '404.html')


def up_and_down(request):
    res = {'code': 100, 'msg': '点赞成功'}
    if request.user.is_authenticated:
        article_id = request.POST.get('article_id')
        is_diggit = json.loads(request.POST.get('up_or_down'))
        count = BlogUpAndDown.objects.filter(user=request.user, blog_article_id=article_id).count()
        if count:
            res['code'] = 101
            res['msg'] = '您已经支持过了'
            return JsonResponse(res)
        else:
            with transaction.atomic():
                BlogUpAndDown.objects.create(is_diggit=is_diggit, user=request.user, blog_article_id=article_id)
                if is_diggit:
                    BlogArticle.objects.filter(pk=article_id).update(up_num=F('up_num') + 1)
                else:
                    BlogArticle.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
        return JsonResponse(res)
    else:
        res['code'] = 102
        res['msg'] = '您没有登录，请先登录<a href="/login/">登录</a>'
        return JsonResponse(res)


def article_detail(request, name, pk):
    user = User.objects.filter(username=name).first()
    article = BlogArticle.objects.filter(pk=pk).first()
    comment_list = BlogComment.objects.filter(blog_article=article)
    if user and article:
        return render(request, 'article.html', locals())
    else:
        return render(request, '404.html')


def comment(request):
    res = {'code': 100, 'msg': '评论成功'}
    if request.user.is_authenticated:
        article_id = request.POST.get('article_id')
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        with transaction.atomic():
            res_comment = BlogComment.objects.create(user=request.user, blog_article_id=article_id, content=content,
                                                     parent_id=parent_id)
            BlogArticle.objects.filter(pk=article_id).update(comment_num=F('comment_num') + 1)
            res['content'] = content
            res['username'] = request.user.username
            if parent_id:
                res['parent_name'] = res_comment.parent.user.username
        return JsonResponse(res)
    else:
        res['code'] = 102
        res['msg'] = '未登录'
        return JsonResponse(res)


@login_required(login_url='/login/')
def backend(reqeust):
    article_list = BlogArticle.objects.filter(user_blog=reqeust.user.user_blog)
    return render(reqeust, 'backend/index.html', locals())


@login_required(login_url='/login/')
def delete(request):
    pk = request.GET.get('id')
    BlogArticle.objects.filter(pk=pk).delete()
    return redirect('/backend/')


@login_required(login_url='/login/')
def add_article(request):
    if request.method == 'GET':
        category_list = BlogCategory.objects.filter(user_blog=request.user.user_blog)
        tag_list = BlogTag.objects.filter(user_blog=request.user.user_blog)
        return render(request, 'backend/add_article.html', locals())
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        soup = BeautifulSoup(content, 'html.parser')
        description = soup.text.replace('/n', '').replace('/r', '')[:70]
        script_list = soup.findAll('script')
        for script in script_list:
            script.decompose()
        category = request.POST.get('category')
        tags = request.POST.get('tag')
        article = BlogArticle.objects.create(title=title, description=description, content=str(soup),
                                             user_blog=request.user.user_blog, blog_category_id=category)
        article.blog_tag.add(*tags)
        return redirect('/backend/')


import os
from django.conf import settings


def put_img(request):
    img = request.FILES.get('myfile')
    img_name = os.path.join(settings.MEDIA_ROOT, 'upload', img.name)
    with open(img_name, 'wb') as f:
        for line in img:
            f.write(line)

    return JsonResponse(
        {
            "error": 0,
            "url": "http://127.0.0.1:8000/media/upload/" + img.name
        })


@login_required(login_url='/login/')
def edit_article(request):
    if request.method == 'GET':
        article_id = request.GET.get('id')
        article = BlogArticle.objects.filter(pk=article_id).first()
        category_list = BlogCategory.objects.filter(user_blog=request.user.user_blog)
        tag_list = BlogTag.objects.filter(user_blog=request.user.user_blog)
        return render(request, 'backend/edit_article.html', locals())


from django.contrib.auth import logout as out


def logout(request):
    out(request)
    return redirect('/')


def update_head(request):
    if request.method == 'GET':
        return render(request, 'backend/update_head.html')
    else:
        head_file = request.FILES.get('head_file')
        request.user.head = head_file
        request.user.save()
        return redirect('/backend/')


def update_pwd(request):
    if request.method == 'GET':
        return render(request, 'backend/update_pwd.html')
    else:
        old_pwd = request.POST.get('old_pwd')
        new_pwd = request.POST.get('new_pwd')
        confirm_pwd = request.POST.get('confirm_pwd')
        if request.user.check_password(old_pwd):
            if new_pwd == confirm_pwd:
                request.user.set_password(new_pwd)
                request.user.save()
                logout(request)
                return redirect('/')
            else:
                return render(request, 'backend/update_pwd.html', context={'error': '两次输入密码不一致'})
        else:
            return render(request, 'backend/update_pwd.html', context={'error': '原密码输入错误'})
