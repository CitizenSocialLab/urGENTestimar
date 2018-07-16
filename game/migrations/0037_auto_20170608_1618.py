# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0036_game'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='game',
            new_name='name',
        ),
    ]
