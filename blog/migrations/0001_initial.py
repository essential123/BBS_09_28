# Generated by Django 2.2 on 2022-09-28 08:56

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=32, null=True)),
                ('head', models.FileField(default='head/default.png', upload_to='head')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name_plural': '?????????',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='?????????')),
                ('img', models.FileField(default='/static/default.jpg', upload_to='banner')),
                ('link', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name_plural': '?????????',
            },
        ),
        migrations.CreateModel(
            name='BlogArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='?????????')),
                ('description', models.CharField(max_length=255, verbose_name='????????????')),
                ('content', models.TextField(verbose_name='????????????')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='????????????')),
                ('up_num', models.IntegerField(default=0)),
                ('down_num', models.IntegerField(default=0)),
                ('comment_num', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': '??????',
            },
        ),
        migrations.CreateModel(
            name='UserBlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, null=True, verbose_name='????????????')),
                ('site_name', models.CharField(max_length=32, null=True, verbose_name='?????????')),
                ('site_style', models.CharField(max_length=32, null=True, verbose_name='??????????????????')),
            ],
            options={
                'verbose_name_plural': '??????',
            },
        ),
        migrations.CreateModel(
            name='BlogUpAndDown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_diggit', models.BooleanField(verbose_name='??????????????????')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('blog_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.BlogArticle')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '??????',
            },
        ),
        migrations.CreateModel(
            name='BlogTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='?????????')),
                ('user_blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.UserBlog')),
            ],
            options={
                'verbose_name_plural': '??????',
            },
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=64, verbose_name='????????????')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('blog_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.BlogArticle')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.BlogComment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '??????',
            },
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='?????????')),
                ('user_blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.UserBlog')),
            ],
            options={
                'verbose_name_plural': '??????',
            },
        ),
        migrations.AddField(
            model_name='blogarticle',
            name='blog_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.BlogCategory', verbose_name='??????'),
        ),
        migrations.AddField(
            model_name='blogarticle',
            name='blog_tag',
            field=models.ManyToManyField(to='blog.BlogTag', verbose_name='??????'),
        ),
        migrations.AddField(
            model_name='blogarticle',
            name='user_blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.UserBlog', verbose_name='??????'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_blog',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.UserBlog'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
