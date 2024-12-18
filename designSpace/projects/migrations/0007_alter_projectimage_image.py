# Generated by Django 5.1.3 on 2024-12-15 09:37

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_project_cover_image_public_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectimage',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
