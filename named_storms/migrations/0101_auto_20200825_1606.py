# Generated by Django 3.0.5 on 2020-08-25 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('named_storms', '0100_nsempsadata_geo_hash'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='nsempsadata',
            index=models.Index(fields=['nsem_psa_variable', 'geo_hash', 'date', 'value'], name='named_storm_nsem_ps_665426_idx'),
        ),
    ]