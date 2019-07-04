from django.db import models
import json

# Create your models here.
class BaseModel(models.Model):
    name = models.CharField(max_length=32,null=True)
    remark = models.TextField(default='',null=True,blank=True,verbose_name='备注')
    # create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    # update_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')

    @property
    def to_dict_base(self):
        ret = {}
        for attr in [f.name for f in self._meta.fields]:
            value = getattr(self,attr)
            ret[attr] = value
        return ret

    def __str__(self):
        return self.name

    class Meta:
        abstract = True #抽象类

class Idc(BaseModel):
    '''
    机房表
    '''
    address = models.CharField(max_length=64)
    phone = models.CharField(max_length=64,null=True,blank=True,default='0')

    class Meta:
        unique_together = ('name',)

    @property
    def to_dict(self):
        ret = self.to_dict_base
        objects = self.rack_set.all()
        # print("objects:" , objects.values())
        ret['racks'] = {'data':[obj for obj in objects.values()],'count':objects.count()}
        # print("ret",ret)
        return ret

class Rack(BaseModel):
    '''
    机柜表
    '''
    idc = models.ForeignKey(Idc,null=True,blank=True,default='',on_delete=models.SET_DEFAULT,verbose_name='所属机房')
    number = models.CharField(max_length=64,null=True,blank=True,default='',verbose_name='编号')
    size = models.CharField(max_length=16,null=True,blank=True,default='',verbose_name='尺寸')

    class Meta:
        unique_together = ('name','idc')

    @property
    def to_dict(self):
        ret = self.to_dict_base
        ret['col1'] = '111'
        idc = getattr(self,'idc')
        # print("idc:",idc.id)
        # print(idc)
        idc_data = idc.to_dict_base if idc else {}
        # print("idc_data: ",idc_data)
        ret['idc'] = idc_data
        objects = self.server_set.all()
        ret['servers'] = {'data':[obj for obj in objects.values()],'count':objects.count()}
        # print(ret)
        return ret

class Server(BaseModel):
    STATUS = (
        (0, u'下线'),
        (1, u'上线'),
    )
    rack = models.ForeignKey(Rack,default='',null=True,blank=True,on_delete=models.SET_DEFAULT,verbose_name='所属机柜')
    uuid = models.CharField(default='',max_length=128,null=True,blank=True,verbose_name='UUID')
    cpu = models.CharField(default='',max_length=64,null=True,blank=True,verbose_name='CPU')
    memory = models.CharField(default='',max_length=64,null=True,blank=True,verbose_name='内存')
    disk = models.CharField(default='',max_length=64,null=True,blank=True,verbose_name='磁盘大小')
    ip = models.CharField(default='',max_length=64,null=True,blank=True,verbose_name='ip地址')
    business = models.CharField(default='',max_length=64,null=True,blank=True,verbose_name='业务线')
    server_type = models.CharField(default='',max_length=128,null=True,blank=True,verbose_name='服务器类型')
    daq = models.TextField(default='',null=True,blank=True,verbose_name='数据采集')
    status = models.IntegerField(default=1,choices=STATUS,verbose_name='运行状态')
    os = models.CharField(default='',max_length=64,null=True,blank=True,verbose_name='操作系统')

    class Meta:
        unique_together = ('uuid', 'server_type')
        ordering = ['-ip']

    @property
    def to_dict(self):
        ret = self.to_dict_base
        rack = getattr(self, 'rack')
        rack_data = rack.to_dict if rack else {}
        ret['rack'] = rack_data
        # ret['count'] = '123'
        daq = eval(self.daq) if self.daq else ''
        # print(type(daq))
        ret['daq'] = daq
        ret['daq_json'] = json.dumps(daq)
        return ret


