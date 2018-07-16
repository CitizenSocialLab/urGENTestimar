# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0056_auto_20170724_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bot_pr1_dictator1',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='bot_pr1_prisoner1',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='bot_pr1_prisoner2',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='bot_pr1_snowdrift1',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
