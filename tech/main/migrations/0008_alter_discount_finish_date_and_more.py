# Generated by Django 4.2.3 on 2023-07-24 12:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_discount_finish_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='finish_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 24, 15, 54, 11, 9833, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='popularity',
            name='finish_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 24, 15, 54, 11, 9833, tzinfo=datetime.timezone.utc)),
        ),
    ]
