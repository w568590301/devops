# Generated by Django 2.0.8 on 2019-06-20 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0012_auto_20190619_0243'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='server',
            unique_together={('uuid', 'server_type')},
        ),
    ]
