# Generated by Django 2.0.5 on 2019-09-17 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('named_storms', '0055_auto_20190911_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nsempsauserexport',
            name='format',
            field=models.CharField(choices=[('netcdf', 'netcdf'), ('shapefile', 'shapefile'), ('geojson', 'geojson'), ('csv', 'csv')], max_length=30),
        ),
    ]
