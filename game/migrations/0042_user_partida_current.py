# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0041_auto_20170608_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='partida_current',
            field=models.ForeignKey(related_name='current', to='game.Partida', null=True),
        ),
    ]
