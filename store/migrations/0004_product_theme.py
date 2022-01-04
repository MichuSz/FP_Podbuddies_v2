# Generated by Django 4.0 on 2022-01-04 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_theme_alter_product_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='theme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.theme'),
        ),
    ]
