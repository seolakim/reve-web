# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-30 00:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('foodle', '0002_delete_foodle'),
    ]

    operations = [
        migrations.CreateModel(
            name='gn',
            fields=[
                ('url', models.URLField(primary_key=True, serialize=False, unique=True, verbose_name='url')),
                ('ind', models.CharField(max_length=1024)),
                ('title', models.CharField(max_length=1024)),
                ('subtitle', models.CharField(max_length=2048)),
                ('data', models.CharField(max_length=1024)),
                ('photo', models.CharField(max_length=1024)),
            ],
        ),
    ]