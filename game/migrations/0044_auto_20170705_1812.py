# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0043_auto_20170609_1544'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='estat_civil',
        ),
        migrations.RemoveField(
            model_name='user',
            name='nivell_estudis',
        ),
        migrations.RemoveField(
            model_name='user',
            name='origen',
        ),
        migrations.RemoveField(
            model_name='user',
            name='pais',
        ),
        migrations.RemoveField(
            model_name='user',
            name='residencia',
        ),
        migrations.RemoveField(
            model_name='user',
            name='situacio_laboral',
        ),
    ]
