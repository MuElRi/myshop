# Generated by Django 4.2.16 on 2024-12-15 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='type',
            field=models.CharField(blank=True, choices=[('image', 'Image'), ('video', 'Video')], max_length=10),
        ),
    ]
