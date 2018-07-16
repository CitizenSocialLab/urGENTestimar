# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0044_auto_20170705_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pr1',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
