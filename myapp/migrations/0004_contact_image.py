# Generated by Django 4.1 on 2022-08-25 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='image',
            field=models.ImageField(default='', upload_to='media/contact/'),
            preserve_default=False,
        ),
    ]