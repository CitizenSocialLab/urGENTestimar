# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0053_auto_20170711_1016'),
    ]

    operations = [
        migrations.CreateModel(
            name='Snowdrift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seleccio1', models.CharField(default=b'', max_length=1)),
                ('is_robot1', models.BooleanField(default=True)),
                ('data_seleccio1', models.DateTimeField(null=True)),
                ('diners_guanyats1', models.FloatField(default=0)),
                ('partida', models.ForeignKey(to='game.Partida', null=True)),
                ('rival1', models.ForeignKey(related_name='rival_snowdrift1', blank=True, to='game.User', null=True)),
                ('user', models.ForeignKey(to='game.User')),
            ],
        ),
    ]
