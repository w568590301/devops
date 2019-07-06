from django.db import models
from account.models import User
# Create your models here.

class BaseModel(models.Model):
    '''
    基础表（抽象类）
    '''
    name = models.CharField(max_length=32,verbose_name='名字')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    remark = models.TextField(default='',null=True,blank=True,verbose_name='备注')

    @property
    def to_dict_base(self):
        ret = dict()
        for attr in [f.name for f in self._meta.fields]:
            value = getattr(self,attr)
            ret[attr] = value
        return ret

    def __str__(self):
        return self.name

    class Meta:
        abstract = True #抽象类
        ordering = ['-id'] #ID倒排

class InceptionSql(BaseModel):
    SQL_STATUS = (
        (-2,'已回滚'),
        (-1,'待执行'),
        (0,'执行成功'),
        (1,'已放弃'),
        (2,'执行失败'),
    )

    ENV = (
        (1,'生产环境'),
        (2,'测试环境')
    )

    sql_users = models.ManyToManyField(User)
    committer = models.CharField(max_length=20)
    sql_content = models.TextField(blank=True,null=True)
    env = models.IntegerField(choices=ENV)
    db_name = models.CharField(max_length=50)
    treater = models.CharField(max_length=20)
    status = models.IntegerField(default=-1,choices=SQL_STATUS)
    execute_info = models.TextField(default='',null=True,blank=True)
    exe_affected_rows = models.CharField(max_length=10)
    roll_affected_rows = models.CharField(max_length=10)
    rollback_id = models.TextField(blank=True,null=True)
    rollback_db = models.CharField(max_length=100)

    @property
    def to_dict(self):
        ret = self.to_dict_base
        return ret

class DBConf(BaseModel):
    GENDER_CHOICES = (
        (1,'生产'),
        (2,'测试'),
    )
    user = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    host = models.CharField(max_length=16)
    port = models.CharField(max_length=8)
    env = models.IntegerField(blank=True,null=True,choices=GENDER_CHOICES)

    class Meta:
        unique_together = ('name','host','env','port')
        ordering = ['-id']

