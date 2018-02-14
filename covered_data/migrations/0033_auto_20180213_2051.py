# Generated by Django 2.0.1 on 2018-02-13 20:51

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covered_data', '0032_auto_20180213_2049'),
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
        migrations.AddField(
            model_name='namedstormcovereddata',
            name='geo',
            field=django.contrib.gis.db.models.fields.GeometryField(geography=True, null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='namedstormcovereddata',
            name='time_end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='namedstormcovereddata',
            name='time_start',
            field=models.DateTimeField(null=True),
        ),
    ]
