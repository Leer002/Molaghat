# Generated by Django 4.2 on 2025-01-18 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carts', '0003_alter_cartitems_date_added'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('avatar', models.ImageField(blank=True, upload_to='gateways/', verbose_name='avatar')),
                ('is_enable', models.BooleanField(default=True, verbose_name='is enable')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='updated time')),
            ],
            options={
                'verbose_name': 'Gateway',
                'verbose_name_plural': 'Gateways',
                'db_table': 'gateways',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='price')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Void'), (10, 'Paid'), (20, 'Error'), (30, 'User Canceled'), (31, 'Refunded')], default=0, verbose_name='status')),
                ('device_uuid', models.CharField(blank=True, max_length=40, verbose_name='device uuid')),
                ('token', models.CharField(blank=True, max_length=20, verbose_name='token')),
                ('phone_number', models.BigIntegerField(help_text='.با 98 شماره تلفن را شروع کنید', validators=[utils.validators.PhoneNumberValidator()], verbose_name='phone number')),
                ('consumed_code', models.PositiveIntegerField(null=True, verbose_name='consumed code')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='modification time')),
                ('gateway', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='payments.gateway', verbose_name='gateway')),
                ('items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='carts.cartitems', verbose_name='items')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
                'db_table': 'payments',
            },
        ),
    ]
