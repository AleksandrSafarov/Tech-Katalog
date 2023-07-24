# Generated by Django 4.2.3 on 2023-07-23 11:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyers', '0006_alter_comment_date_alter_productincart_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favourites',
            options={'verbose_name_plural': 'Favourites'},
        ),
        migrations.AlterModelOptions(
            name='productincart',
            options={'verbose_name_plural': 'Products in cart'},
        ),
        migrations.AlterModelOptions(
            name='savedaddress',
            options={'verbose_name_plural': 'Saved addresses'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 23, 14, 21, 27, 952846, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='productincart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 23, 14, 21, 27, 952846, tzinfo=datetime.timezone.utc)),
        ),
    ]
