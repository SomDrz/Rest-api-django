# Generated by Django 5.1.4 on 2024-12-24 08:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_reviewproduct_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewproduct',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='product.product'),
        ),
    ]
