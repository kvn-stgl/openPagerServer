# Generated by Django 2.1.2 on 2018-10-11 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pager', '0015_remove_idiom_from_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pager.Organization'),
        ),
    ]