# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0051_user_check1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='pr4',
            new_name='feeling',
        ),
        migrations.AddField(
            model_name='user',
            name='interest',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
