# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0040_auto_20170608_1644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='partida_01',
        ),
        migrations.AddField(
            model_name='user',
            name='partida_dictator',
            field=models.ForeignKey(related_name='dictator', to='game.Partida', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='partida_prisoner',
            field=models.ForeignKey(related_name='prisoner', to='game.Partida', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='partida_trust',
            field=models.ForeignKey(related_name='trust', to='game.Partida', null=True),
        ),
    ]
