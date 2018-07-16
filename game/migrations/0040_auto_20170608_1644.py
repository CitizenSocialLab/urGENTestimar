# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0039_auto_20170608_1643'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='partida',
            new_name='partida_01',
        ),
    ]
