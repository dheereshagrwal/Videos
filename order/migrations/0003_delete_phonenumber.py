# Generated by Django 4.0.1 on 2022-01-11 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_transid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PhoneNumber',
        ),
    ]
