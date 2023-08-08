# Generated by Django 4.2.3 on 2023-08-06 17:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_discount_finish_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productrating',
            options={},
        ),
        migrations.AlterModelOptions(
            name='sellerrating',
            options={},
        ),
        migrations.AddField(
            model_name='productrating',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 6, 20, 59, 16, 310105, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='productrating',
            name='text',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='sellerrating',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 6, 20, 59, 16, 313169, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='sellerrating',
            name='text',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='finish_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 6, 20, 59, 16, 308243, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='popularity',
            name='finish_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 6, 20, 59, 16, 314169, tzinfo=datetime.timezone.utc)),
        ),
    ]
