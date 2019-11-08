
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

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']

    def __str__(self):
        return self.title
