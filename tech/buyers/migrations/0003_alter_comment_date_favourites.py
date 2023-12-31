# Generated by Django 4.2.3 on 2023-07-20 09:38

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_category_plural_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('buyers', '0002_alter_comment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 20, 12, 38, 1, 655869, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
