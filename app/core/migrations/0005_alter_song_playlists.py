# Generated by Django 3.2.9 on 2021-11-25 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_song'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='playlists',
            field=models.ManyToManyField(blank=True, to='core.PlayList'),
        ),
    ]
