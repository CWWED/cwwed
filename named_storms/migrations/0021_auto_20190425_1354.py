# Generated by Django 2.0.5 on 2019-04-25 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('named_storms', '0020_nsempsavariable_color_bar'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='nsempsavariable',
            unique_together={('nsem', 'name')},
        ),
    ]
