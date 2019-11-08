from django.db import models


class BaseModel(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0

    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        abstract = True
