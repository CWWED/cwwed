# Generated by Django 2.0.5 on 2019-04-26 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('named_storms', '0021_auto_20190425_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='nsempsavariable',
            name='geo_type',
            field=models.CharField(choices=[('multipolygon', 'MultiPolygon'), ('point', 'Point')], default='multipolygon', max_length=20),
            preserve_default=False,
        ),
    ]
