# Generated by Django 4.0.1 on 2022-01-07 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewrating',
            name='review_image',
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/reviews')),
                ('review_rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='review.reviewrating')),
            ],
        ),
    ]