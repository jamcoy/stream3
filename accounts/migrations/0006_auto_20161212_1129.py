# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-12 11:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20161212_1024'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='image',
            new_name='profile_image',
        ),
    ]
