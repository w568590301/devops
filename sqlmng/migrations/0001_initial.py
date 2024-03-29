# Generated by Django 2.0.8 on 2019-07-05 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DBConf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='名字')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('remark', models.TextField(blank=True, default='', null=True, verbose_name='备注')),
                ('user', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=128)),
                ('host', models.CharField(max_length=16)),
                ('port', models.CharField(max_length=8)),
                ('env', models.IntegerField(blank=True, choices=[(1, '生产'), (2, '测试')], null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='dbconf',
            unique_together={('name', 'host', 'env', 'port')},
        ),
    ]
