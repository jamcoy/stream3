# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-08 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='public_name',
            field=models.CharField(default='Nameless', max_length=20),
            preserve_default=False,
        ),
    ]
