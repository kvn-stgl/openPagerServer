# Generated by Django 2.1.1 on 2018-09-17 10:29

from django.db import migrations, models
import pager.models


class Migration(migrations.Migration):

    dependencies = [
        ('pager', '0003_auto_20180914_1712'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='invite_reason',
        ),
        migrations.AddField(
            model_name='membership',
            name='role',
            field=models.CharField(default='I', max_length=1),
        ),
    ]
