# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0054_snowdrift'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partida',
            name='control',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='data_fi_ronda',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='guanyen_igualment',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='num_rondes',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='objectiu_aconseguit',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='ronda_actual',
        ),
    ]
