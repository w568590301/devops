# Generated by Django 2.0.8 on 2019-06-19 02:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0011_remove_server_hostname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server',
            old_name='server_cpu',
            new_name='cpu',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='server_disk',
            new_name='disk',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='server_memory',
            new_name='memory',
        ),
    ]
