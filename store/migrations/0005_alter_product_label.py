# Generated by Django 4.0 on 2022-01-04 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='label',
            field=models.CharField(blank=True, choices=[('N', 'New'), ('BS', 'Best Seller')], max_length=2, null=True),
        ),
    ]
