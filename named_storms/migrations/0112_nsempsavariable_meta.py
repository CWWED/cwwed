# Generated by Django 3.0.5 on 2020-11-21 13:50

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('named_storms', '0111_nsempsamanifestdataset_topology_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='nsempsavariable',
            name='meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
    ]
