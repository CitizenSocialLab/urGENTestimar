# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0058_auto_20170725_1540'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='codi_postal',
            new_name='on_vius',
        ),
    ]
