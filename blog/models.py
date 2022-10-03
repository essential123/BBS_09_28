from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=32, null=True)
    head = models.FileField(upload_to='head', default='head/default.png')
    user_blog = models.OneToOneField(to='UserBlog', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = '用户表'


class UserBlog(models.Model):
    title = models.CharField(max_length=32, null=True, verbose_name='博客标题')
    site_name = models.CharField(max_length=32, null=True, verbose_name='副标题')
    site_style = models.CharField(max_length=32, null=True, verbose_name='个人站点样式')

    class Meta:
        verbose_name_plural = '博客'

    def __str__(self):
        return self.title


class BlogTag(models.Model):
    name = models.CharField(max_length=32, verbose_name='标题名')
    user_blog = models.ForeignKey(to='UserBlog', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class BlogCategory(models.Model):
    name = models.CharField(max_length=32, verbose_name='分类名')
    user_blog = models.ForeignKey(to='UserBlog', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '分类'

    def __str__(self):
        return self.name


class BlogArticle(models.Model):
    title = models.CharField(max_length=32, verbose_name='文章名')
    description = models.CharField(max_length=255, verbose_name='文章摘要')
    content = models.TextField(verbose_name='文章内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    up_num = models.IntegerField(default=0)
    down_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)

    blog_tag = models.ManyToManyField(to='BlogTag', verbose_name='标签')
    user_blog = models.ForeignKey(to='UserBlog', on_delete=models.CASCADE, verbose_name='博客')
    blog_category = models.ForeignKey(to='BlogCategory', on_delete=models.CASCADE, verbose_name='分类')

    class Meta:
        verbose_name_plural = '文章'

    def __str__(self):
        try:
            return '文章名:%s， 博客：%s' % (self.title, self.user_blog.title)
        except:
            return self.title


class BlogUpAndDown(models.Model):
    is_diggit = models.BooleanField(verbose_name='点赞或者点踩')
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to='User', on_delete=models.CASCADE)
    blog_article = models.ForeignKey(to='BlogArticle', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '点赞'


class BlogComment(models.Model):
    content = models.CharField(max_length=64, verbose_name='评论内容')
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to='User', on_delete=models.CASCADE)
    blog_article = models.ForeignKey(to='BlogArticle', on_delete=models.CASCADE)
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = '评论'


class Banner(models.Model):
    name = models.CharField(max_length=32, verbose_name='轮播图')
    img = models.FileField(upload_to='banner', default='/static/default.jpg')
    link = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = '轮播图'
