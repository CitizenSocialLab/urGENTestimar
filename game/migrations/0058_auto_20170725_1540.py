# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0057_auto_20170725_1145'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='diners_total',
            new_name='punts_totals',
        ),
        migrations.RemoveField(
            model_name='user',
            name='diners_actuals',
        ),
        migrations.RemoveField(
            model_name='user',
            name='diners_inicials',
        ),
    ]
