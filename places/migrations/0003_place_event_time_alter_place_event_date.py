# Generated by Django 4.2 on 2025-01-07 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='event_time',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='event time'),
        ),
        migrations.AlterField(
            model_name='place',
            name='event_date',
            field=models.CharField(max_length=50, verbose_name='event date'),
        ),
    ]
