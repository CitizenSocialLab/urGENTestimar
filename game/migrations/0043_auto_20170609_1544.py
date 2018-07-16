# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0042_user_partida_current'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='data_finalitzacio',
            new_name='data_finalitzacio_04',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='data_registre',
            new_name='data_finalitzacio_05',
        ),
        migrations.AddField(
            model_name='user',
            name='data_finalitzacio_dictator',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='data_finalitzacio_prisoner',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='data_finalitzacio_trust',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='data_registre_04',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='data_registre_05',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='data_registre_dictator',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='data_registre_prisoner',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='data_registre_trust',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='partida_04',
            field=models.ForeignKey(related_name='nom_04', to='game.Partida', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='partida_05',
            field=models.ForeignKey(related_name='nom_05', to='game.Partida', null=True),
        ),
    ]
