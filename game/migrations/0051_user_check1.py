# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0050_auto_20170707_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='check1',
            field=models.BooleanField(default=False),
        ),
    ]
