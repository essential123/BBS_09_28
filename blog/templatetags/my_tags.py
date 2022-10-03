from blog.models  import User, BlogArticle, UserBlog, BlogTag, BlogCategory, BlogUpAndDown, BlogComment, Banner
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django import template
register=template.Library()

@register.inclusion_tag('left.html',name='left')
def left(name):
    user_obj = User.objects.all().filter(username=name).first()
    category_res = BlogCategory.objects.all().filter(user_blog=user_obj.user_blog).values('id').annotate(
        c=Count('blogarticle__id')).values_list('id', 'name', 'c')
    tag_res = BlogTag.objects.all().filter(user_blog=user_obj.user_blog).values('id').annotate(c=Count('blogarticle__id')).values_list(
        'id', 'name', 'c')
    date_res = BlogArticle.objects.all().filter(user_blog=user_obj.user_blog).annotate(year_month=TruncMonth('create_time')).values(
        'year_month').annotate(c=Count('id')).values_list('year_month', 'c')
    # print(tag_res)
    # print(category_res)
    # print(date_res)
    return {'tag_res':tag_res,'category_res':category_res,'date_res':date_res,'user':user_obj}