# Generated by Django 2.0.5 on 2019-09-11 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('named_storms', '0053_auto_20190911_1602'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nsempsa',
            old_name='date_processed',
            new_name='date_psa_processed',
        ),
    ]
