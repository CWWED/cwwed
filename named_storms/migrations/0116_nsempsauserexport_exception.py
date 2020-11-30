# Generated by Django 3.1.3 on 2020-11-30 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('named_storms', '0115_nsempsauserexport_success'),
    ]

    operations = [
        migrations.AddField(
            model_name='nsempsauserexport',
            name='exception',
            field=models.CharField(blank=True, help_text='message for an unsuccessful export', max_length=1000, null=True),
        ),
    ]