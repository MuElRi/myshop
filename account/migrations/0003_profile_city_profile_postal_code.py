# Generated by Django 4.2.16 on 2024-12-03 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_profile_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='postal_code',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
    ]
