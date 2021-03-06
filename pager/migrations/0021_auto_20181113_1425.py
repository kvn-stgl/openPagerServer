# Generated by Django 2.1.3 on 2018-11-13 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pager', '0020_operationloop_operation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operation',
            old_name='guid',
            new_name='operation_guid',
        ),
        migrations.AlterField(
            model_name='operationpropertylocation',
            name='geo_latitude',
            field=models.DecimalField(decimal_places=30, max_digits=42, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='operationpropertylocation',
            name='geo_longitude',
            field=models.DecimalField(decimal_places=30, max_digits=42, null=True, verbose_name='Longitude'),
        ),
    ]
