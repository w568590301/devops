# Generated by Django 2.0.8 on 2019-06-18 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0003_rack'),
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, null=True)),
                ('remark', models.TextField()),
                ('uuid', models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='UUID')),
                ('cpu', models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='CPU')),
                ('memory', models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='内存')),
                ('disk', models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='磁盘大小')),
                ('ip', models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='ip地址')),
                ('business', models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='业务线')),
                ('server_type', models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='服务器类型')),
                ('daq', models.TextField(blank=True, default='', null=True, verbose_name='数据采集')),
                ('status', models.IntegerField(choices=[(0, '下线'), (1, '上线')], default=1, verbose_name='运行状态')),
                ('rack', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='cmdb.Rack', verbose_name='所属机柜')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
