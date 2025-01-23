# Generated by Django 4.2 on 2025-01-23 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_alter_cartitems_is_purchased'),
        ('subscriptions', '0003_remove_subscription_items_subscription_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='items',
        ),
        migrations.AddField(
            model_name='subscription',
            name='items',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='carts.cartitems', verbose_name='items'),
        ),
    ]
