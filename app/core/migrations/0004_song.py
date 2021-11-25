# Generated by Django 3.2.9 on 2021-11-25 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_singer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('length', models.DecimalField(decimal_places=2, max_digits=4)),
                ('release', models.DateTimeField()),
                ('playlists', models.ManyToManyField(to='core.PlayList')),
                ('singers', models.ManyToManyField(to='core.Singer')),
            ],
        ),
    ]
