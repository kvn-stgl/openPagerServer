# Generated by Django 2.1.1 on 2018-09-17 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pager', '0007_auto_20180917_1557'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('user', 'organization')},
        ),
    ]