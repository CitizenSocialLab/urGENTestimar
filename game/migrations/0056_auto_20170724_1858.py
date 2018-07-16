# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0055_auto_20170712_1353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='feeling_dictator2',
            new_name='feeling_prisoner2',
        ),
    ]
