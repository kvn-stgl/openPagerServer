# Generated by Django 2.1.1 on 2018-09-11 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pager', '0002_auto_20180911_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarm',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alarm',
            name='receivers',
            field=models.ManyToManyField(related_name='receivers', to=settings.AUTH_USER_MODEL),
        ),
    ]
