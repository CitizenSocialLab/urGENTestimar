# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0060_auto_20170728_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='data_last_action',
            field=models.DateTimeField(null=True),
        ),
    ]
