# Generated by Django 4.2.3 on 2023-07-18 10:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('is_sertificated', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to='images/sellers/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]