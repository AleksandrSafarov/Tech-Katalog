# Generated by Django 4.2.3 on 2023-07-27 10:11

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buyers', '0011_alter_comment_date_alter_productincart_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productincart',
            options={'verbose_name_plural': 'Product in cart'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 27, 13, 11, 4, 581879, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='productincart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 27, 13, 11, 4, 580879, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='ProductInOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buyers.savedaddress')),
                ('productInCart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buyers.productincart')),
            ],
            options={
                'verbose_name_plural': 'Product in order',
            },
        ),
    ]
