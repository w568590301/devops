# Generated by Django 2.0.8 on 2019-06-29 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0016_auto_20190629_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='status',
            field=models.IntegerField(choices=[(0, '下线'), (1, '上线')], default=0, verbose_name='运行状态'),
        ),
    ]
