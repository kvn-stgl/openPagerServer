# Generated by Django 2.1.1 on 2018-09-26 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pager', '0009_auto_20180921_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarm',
            name='keyword',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Stichwort'),
        ),
        migrations.AlterField(
            model_name='alarm',
            name='destination',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Einsatzadresse'),
        ),
        migrations.AlterField(
            model_name='alarm',
            name='destination_lat',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='alarm',
            name='destination_lng',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='alarm',
            name='message',
            field=models.TextField(verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='alarm',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Titel'),
        ),
    ]
