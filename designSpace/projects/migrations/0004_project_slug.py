# Generated by Django 5.1.3 on 2024-11-28 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_remove_project_image_library_alter_project_area_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
