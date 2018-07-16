# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0047_auto_20170705_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='dictator',
            name='partida',
            field=models.ForeignKey(to='game.Partida', null=True),
        ),
        migrations.AddField(
            model_name='prisoner',
            name='partida',
            field=models.ForeignKey(to='game.Partida', null=True),
        ),
    ]
