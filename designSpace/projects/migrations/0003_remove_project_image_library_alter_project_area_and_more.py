# Generated by Django 5.1.3 on 2024-11-26 21:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_project_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='image_library',
        ),
        migrations.AlterField(
            model_name='project',
            name='area',
            field=models.PositiveIntegerField(blank=True, help_text='Area in square meters', null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='cover_image',
            field=models.ImageField(upload_to='project_images/cover/'),
        ),
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='project_images/gallery/')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='projects.project')),
            ],
        ),
    ]