from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    ROLES = (
        ('1', u'总监'),
        ('2', u'经理'),
        ('3', u'研发'),
    )
    leader = models.ForeignKey('User', null=True, blank=True, on_delete=models.CASCADE, related_name='leader_devs')
    admin_mail = models.ForeignKey('User', null=True, blank=True, on_delete=models.CASCADE, related_name='admin_devs')
    role = models.CharField(max_length=32, default='developer', choices=ROLES)
    mail_list_extend = models.TextField(null=True, blank=True)
    remark = models.CharField(max_length=128, default='', blank=True)

    class Meta:
        verbose_name_plural = u'用户'

    def __str__(self):
        return self.username

    @property
    def to_dict(self):
        ret = dict()
        for attr in [f.name for f in self._meta.fields]:
            value = getattr(self,attr)
            ret[attr] = value
        group = self.groups.first()
        ret['group'] = group.name if group else ''
        return ret
