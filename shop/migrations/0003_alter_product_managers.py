# Generated by Django 4.2.16 on 2024-12-13 06:51

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_product_price'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('published', django.db.models.manager.Manager()),
            ],
        ),
    ]