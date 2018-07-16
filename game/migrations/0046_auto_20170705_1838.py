# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0045_user_pr1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='pr1',
            new_name='pr4',
        ),
    ]
