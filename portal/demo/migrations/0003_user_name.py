# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-15 03:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0002_auto_20160415_0226'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=40, null=True),
        ),
    ]