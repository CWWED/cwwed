# Generated by Django 2.0.1 on 2018-03-22 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('named_storms', '0006_nsem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nsem',
            name='model_input',
            field=models.TextField(blank=True),
        ),
    ]
