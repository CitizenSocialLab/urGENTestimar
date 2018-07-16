# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0059_auto_20170726_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='session_game',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
