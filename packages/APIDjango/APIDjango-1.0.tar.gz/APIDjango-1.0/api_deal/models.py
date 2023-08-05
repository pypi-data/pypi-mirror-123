import datetime

from django.db import models


# Create your models here.


class MyForeignKey(models.ForeignKey):

    def __init__(self, to, on_delete=models.DO_NOTHING, related_name=None, related_query_name=None,
                 limit_choices_to=None, parent_link=False, to_field=None,
                 db_constraint=False, **kwargs):
        super().__init__(to=to, on_delete=on_delete, related_name=related_name,
                         related_query_name=related_query_name,
                         limit_choices_to=limit_choices_to, parent_link=parent_link,
                         to_field=to_field, db_constraint=db_constraint, **kwargs)  # 使用super函数

    def value_from_object(self, obj):
        return {} if obj.pk is None else getattr(obj, self.name)


class MyManyToManyField(models.ManyToManyField):
    def __init__(self, to, related_name=None, related_query_name=None,
                 limit_choices_to=None, symmetrical=None, through=None,
                 through_fields=None, db_constraint=False, db_table=None,
                 swappable=False, **kwargs):
        super().__init__(to, related_name=related_name, related_query_name=related_query_name,
                         limit_choices_to=limit_choices_to, symmetrical=symmetrical, through=through,
                         through_fields=through_fields, db_constraint=db_constraint, db_table=db_table,
                         swappable=swappable, **kwargs)  # 使用super函数


class MyOneToOneField(models.OneToOneField):
    def __init__(self, to, on_delete=models.DO_NOTHING, to_field=None, **kwargs):
        kwargs['db_constraint'] = False
        super().__init__(to=to, on_delete=on_delete, to_field=to_field, **kwargs)  # 使用super函数

    def value_from_object(self, obj):
        return {} if obj.pk is None else getattr(obj, self.name)


class MyModel(models.Model):
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        abstract = True

    def to_dict(self, field_list=None):
        res = {}
        if not isinstance(field_list, list):
            return res
        for f in self._meta.local_fields:
            if f.name not in field_list:
                continue
            value = f.value_from_object(self)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            res[f.name] = value
        return res


# 重写QuerySet
class WithDeleteQuerySet(models.QuerySet):

    def delete(self):
        return super().update(is_delete=True)


class WithDeleteManager(models.Manager):
    # 自定义模型管理器中的方法
    def get_queryset(self):
        return WithDeleteQuerySet(self.model, using=self._db).filter(is_delete=False)


class WithDeleteModel(MyModel):
    is_delete = models.BooleanField(verbose_name="是否删除", default=False)

    class Meta:
        abstract = True

    objects = WithDeleteManager()

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()
