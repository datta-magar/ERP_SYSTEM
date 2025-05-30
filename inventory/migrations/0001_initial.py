# Generated by Django 5.2 on 2025-04-29 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('item_code', models.CharField(max_length=50, unique=True)),
                ('category', models.CharField(max_length=50)),
                ('part_number', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('quantity_in_stock', models.PositiveIntegerField(default=0)),
                ('reorder_level', models.PositiveIntegerField(default=10)),
                ('unit', models.CharField(default='pcs', max_length=20)),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('supplier_name', models.CharField(blank=True, max_length=100)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
