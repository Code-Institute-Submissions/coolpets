# Generated by Django 2.2.10 on 2020-04-13 23:40

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150, null=True)),
                ('address_line_1', models.CharField(max_length=150, null=True)),
                ('address_line_2', models.CharField(blank=True, max_length=150, null=True)),
                ('town_or_city', models.CharField(max_length=150, null=True)),
                ('state', models.CharField(blank=True, max_length=150, null=True)),
                ('postcode', models.CharField(max_length=10, null=True)),
                ('date_ordered', models.DateField(default=datetime.date.today, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('shipped', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingDestination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=50)),
                ('shipping_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('shipping_time', models.CharField(default='1 to 2 weeks', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.Product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cart.ShippingDestination'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
