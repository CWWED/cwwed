# Generated by Django 2.0.1 on 2018-09-05 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('named_storms', '0002_auto_20180905_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='namedstormcovereddata',
            name='date_end',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='namedstormcovereddata',
            name='date_start',
            field=models.DateTimeField(blank=True),
        ),
    ]