# Generated by Django 3.2.9 on 2021-11-25 18:39

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20211125_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='singer',
            name='image',
            field=models.ImageField(null=True, upload_to=core.models.singer_image_file_path),
        ),
    ]
