# Generated by Django 2.0.1 on 2018-02-13 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('covered_data', '0030_auto_20180213_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='namedstormcovereddata',
            name='lat_end',
        ),
        migrations.RemoveField(
            model_name='namedstormcovereddata',
            name='lat_start',
        ),
        migrations.RemoveField(
            model_name='namedstormcovereddata',
            name='lng_end',
        ),
        migrations.RemoveField(
            model_name='namedstormcovereddata',
            name='lng_start',
        ),
    ]
