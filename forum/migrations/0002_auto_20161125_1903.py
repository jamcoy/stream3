# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 19:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Vote',
            new_name='PollVote',
        ),
    ]