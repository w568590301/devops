# Generated by Django 2.0.8 on 2019-06-19 02:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0006_server_hostname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='hostname',
        ),
    ]