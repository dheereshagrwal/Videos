# Generated by Django 4.0.1 on 2022-01-07 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anime_name', models.CharField(max_length=255, unique=True)),
                ('anime_popularity', models.SmallIntegerField(default=0)),
            ],
        ),
    ]
