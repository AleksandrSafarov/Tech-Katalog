# Generated by Django 4.2.3 on 2023-07-19 19:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 19, 22, 17, 51, 281170, tzinfo=datetime.timezone.utc)),
        ),
    ]