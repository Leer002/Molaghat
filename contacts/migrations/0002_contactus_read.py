# Generated by Django 4.2 on 2025-01-17 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='read',
            field=models.BooleanField(default=False, verbose_name='read'),
        ),
    ]
