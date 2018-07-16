# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0037_auto_20170608_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
