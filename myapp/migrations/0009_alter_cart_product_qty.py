# Generated by Django 4.1 on 2022-09-03 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product_qty',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
