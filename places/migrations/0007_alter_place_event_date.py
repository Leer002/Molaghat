# Generated by Django 4.2 on 2025-01-27 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0006_place_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='event_date',
            field=models.DateField(verbose_name='event date'),
        ),
    ]
