# Generated by Django 3.0.8 on 2021-03-12 07:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210312_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='listed_by',
            field=models.ManyToManyField(blank=True, related_name='listing', to=settings.AUTH_USER_MODEL),
        ),
    ]
