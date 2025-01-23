# Generated by Django 4.2 on 2025-01-23 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_alter_cartitems_is_purchased'),
        ('payments', '0003_remove_payment_items_payment_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='payments', to='carts.cartitems', verbose_name='items'),
        ),
    ]
