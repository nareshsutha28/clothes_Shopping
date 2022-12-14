# Generated by Django 4.1 on 2022-08-25 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('mobile', models.PositiveIntegerField()),
                ('city', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('profile', models.ImageField(upload_to='profile/')),
                ('usertype', models.CharField(choices=[('user', 'user'), ('seller', 'seller')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Man',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_dname', models.CharField(max_length=100)),
                ('product_category', models.CharField(choices=[('user', 'user'), ('seller', 'seller')], max_length=100)),
                ('product_price', models.PositiveIntegerField()),
                ('product_discount', models.PositiveIntegerField()),
                ('product_disc', models.TextField()),
                ('product_image', models.ImageField(upload_to='Dress/')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]
