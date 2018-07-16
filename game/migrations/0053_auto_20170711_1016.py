# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0052_auto_20170711_0934'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='feeling',
            new_name='feeling_dictator2',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='interest',
            new_name='interest_dictator1',
        ),
        migrations.AddField(
            model_name='user',
            name='interest_dictator2',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='interest_prisoner1',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='interest_prisoner2',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
