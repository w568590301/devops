# Generated by Django 2.0.8 on 2019-07-01 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0019_server_os'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='server',
            options={'ordering': ['-ip']},
        ),
    ]