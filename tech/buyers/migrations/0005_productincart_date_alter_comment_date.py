# Generated by Django 4.2.3 on 2023-07-20 15:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyers', '0004_alter_comment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='productincart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 20, 18, 16, 19, 939093, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 20, 18, 16, 19, 941489, tzinfo=datetime.timezone.utc)),
        ),
    ]
