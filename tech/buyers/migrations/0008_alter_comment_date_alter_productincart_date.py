# Generated by Django 4.2.3 on 2023-07-24 09:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyers', '0007_alter_favourites_options_alter_productincart_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 24, 12, 21, 41, 77195, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='productincart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 24, 12, 21, 41, 76161, tzinfo=datetime.timezone.utc)),
        ),
    ]