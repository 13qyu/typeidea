from django.db import models

from common.models import BaseModel
from blog.models import Post

# Create your models here.


class Comment(BaseModel):
    target = models.ForeignKey(Post, verbose_name='评论目标')   # 临时设计
    content = models.CharField(max_length=2000, verbose_name='内容')
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    website = models.URLField(verbose_name='网站')
    email = models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(default=BaseModel.STATUS_NORMAL,
                                         choices=BaseModel.STATUS_ITEMS, verbose_name='状态')

    class Meta:
        verbose_name = verbose_name_plural = '评论'


