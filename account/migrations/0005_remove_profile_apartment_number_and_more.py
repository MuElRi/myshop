# Generated by Django 4.2.16 on 2024-12-04 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_profile_apartment_number_profile_house_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='apartment_number',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='house_number',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='street',
        ),
    ]
