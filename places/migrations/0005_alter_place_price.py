# Generated by Django 4.2 on 2025-01-09 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0004_alter_place_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='price',
            field=models.IntegerField(verbose_name='price'),
        ),
    ]
