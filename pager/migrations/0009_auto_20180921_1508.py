# Generated by Django 2.1.1 on 2018-09-21 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pager', '0008_auto_20180917_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='destination',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='alarm',
            name='destination_lat',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='alarm',
            name='destination_lng',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='alarm',
            name='message',
            field=models.TextField(),
        ),
    ]