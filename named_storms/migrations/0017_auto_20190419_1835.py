# Generated by Django 2.0.5 on 2019-04-19 18:35

import datetime
import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('named_storms', '0016_auto_20190419_1740'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nsempsa',
            name='water_level_max',
        ),
        migrations.AddField(
            model_name='nsempsa',
            name='color',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
        migrations.AddField(
            model_name='nsempsa',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 19, 18, 35, 19, 172069)),
        ),
        migrations.AddField(
            model_name='nsempsa',
            name='geo',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(default=None, geography=True, srid=4326),
        ),
        migrations.AddField(
            model_name='nsempsa',
            name='value',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='nsempsa',
            name='variable',
            field=models.CharField(default='TODO', max_length=50),
        ),
        migrations.DeleteModel(
            name='DataContour',
        ),
    ]