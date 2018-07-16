# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0049_auto_20170706_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prisoner',
            name='data_guess2',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='data_guess3',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='data_seleccio2',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='data_seleccio3',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='diners_guanyats2',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='diners_guanyats3',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='guess2',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='guess3',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='is_robot2',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='is_robot3',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='rival2',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='rival3',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='rol2',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='rol3',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='seleccio2',
        ),
        migrations.RemoveField(
            model_name='prisoner',
            name='seleccio3',
        ),
    ]
