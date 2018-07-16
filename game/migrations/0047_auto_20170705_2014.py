# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0046_auto_20170705_1838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ronda',
            name='partida',
        ),
        migrations.RemoveField(
            model_name='trust',
            name='rival1',
        ),
        migrations.RemoveField(
            model_name='trust',
            name='rival2',
        ),
        migrations.RemoveField(
            model_name='trust',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userronda',
            name='ronda',
        ),
        migrations.RemoveField(
            model_name='userronda',
            name='user',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='data_finalitzacio_04',
            new_name='data_finalitzacio_dictator1',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='data_finalitzacio_05',
            new_name='data_finalitzacio_dictator2',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='data_finalitzacio_dictator',
            new_name='data_finalitzacio_prisoner1',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='data_finalitzacio_prisoner',
            new_name='data_finalitzacio_prisoner2',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='data_finalitzacio_trust',
            new_name='data_finalitzacio_snowdrift1',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='data_registre_04',
            new_name='data_registre_dictator1',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='data_registre_05',
            new_name='data_registre_dictator2',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='data_registre_dictator',
            new_name='data_registre_prisoner1',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='data_registre_prisoner',
            new_name='data_registre_prisoner2',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='data_registre_trust',
            new_name='data_registre_snowdrift1',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='diners_dictator',
            new_name='diners_dictator1',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='diners_prisoner',
            new_name='diners_dictator2',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='diners_trust',
            new_name='diners_prisoner1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='diners_clima',
        ),
        migrations.RemoveField(
            model_name='user',
            name='partida_04',
        ),
        migrations.RemoveField(
            model_name='user',
            name='partida_05',
        ),
        migrations.RemoveField(
            model_name='user',
            name='partida_dictator',
        ),
        migrations.RemoveField(
            model_name='user',
            name='partida_prisoner',
        ),
        migrations.RemoveField(
            model_name='user',
            name='partida_trust',
        ),
        migrations.RemoveField(
            model_name='user',
            name='vals',
        ),
        migrations.AddField(
            model_name='user',
            name='diners_prisoner2',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='diners_snowdrift1',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='partida_dictator1',
            field=models.ForeignKey(related_name='dictator1', to='game.Partida', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='partida_dictator2',
            field=models.ForeignKey(related_name='dictator2', to='game.Partida', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='partida_prisoner1',
            field=models.ForeignKey(related_name='prisoner1', to='game.Partida', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='partida_prisoner2',
            field=models.ForeignKey(related_name='prisoner2', to='game.Partida', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='partida_snowdrift1',
            field=models.ForeignKey(related_name='snowdrift1', to='game.Partida', null=True),
        ),
        migrations.DeleteModel(
            name='Ronda',
        ),
        migrations.DeleteModel(
            name='Trust',
        ),
        migrations.DeleteModel(
            name='UserRonda',
        ),
    ]
