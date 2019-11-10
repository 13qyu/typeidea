import mistune

from django.contrib.auth.models import User
from django.db import models

from common.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=50, verbose_name='名称')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(User, verbose_name='作者')
    status = models.PositiveIntegerField(default=BaseModel.STATUS_NORMAL,
                                         choices=BaseModel.STATUS_ITEMS,
                                         verbose_name='状态')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []

        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        return {
            'navs': nav_categories,
            'categories': normal_categories
        }


class Tag(BaseModel):
    name = models.CharField(max_length=10, verbose_name='名称')
    owner = models.ForeignKey(User, verbose_name='作者')
    status = models.PositiveIntegerField(default=BaseModel.STATUS_NORMAL,
                                         choices=BaseModel.STATUS_ITEMS,
                                         verbose_name='状态')

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Post(BaseModel):
    STATUS_DRAFT = 2

    STATUS_ITEMS = (
        (BaseModel.STATUS_NORMAL, '正常'),
        (BaseModel.STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文必须为MarkDown格式')
    category = models.ForeignKey(Category, verbose_name='分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者')
    status = models.PositiveIntegerField(default=BaseModel.STATUS_NORMAL,
                                         choices=STATUS_ITEMS,
                                         verbose_name='状态')

    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    content_html = models.TextField(verbose_name='正文html代码', blank=True, editable=False)

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.content_html = mistune.markdown(self.content)
        super().save(*args, **kwargs)

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')

        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')

        return post_list, category

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-id')
        return queryset

    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')