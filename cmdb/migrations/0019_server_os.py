# Generated by Django 2.0.8 on 2019-06-29 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0018_auto_20190629_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='os',
            field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='操作系统'),
        ),
    ]
