# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-30 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0003_auto_20170430_0338'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='description',
            field=models.CharField(default='File', max_length=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='block',
            name='name',
            field=models.CharField(default='Desc', max_length=50),
            preserve_default=False,
        ),
    ]
