# Generated by Django 4.0 on 2021-12-30 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='img',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]