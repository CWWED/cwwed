# Generated by Django 3.0.5 on 2020-08-27 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('named_storms', '0101_auto_20200825_1606'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='nsempsadata',
            name='named_storm_nsem_ps_665426_idx',
        ),
        migrations.AddIndex(
            model_name='nsempsadata',
            index=models.Index(fields=['nsem_psa_variable', 'point', 'date', 'geo_hash', 'value'], name='named_storm_nsem_ps_a521c8_idx'),
        ),
    ]