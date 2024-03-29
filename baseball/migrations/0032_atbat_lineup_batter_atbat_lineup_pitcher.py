# Generated by Django 4.1.6 on 2023-07-18 01:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseball', '0031_alter_manager_first_name_alter_manager_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='atbat',
            name='lineup_batter',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='at_bats', to='baseball.lineupplayer'),
        ),
        migrations.AddField(
            model_name='atbat',
            name='lineup_pitcher',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='pitched_at_bats', to='baseball.lineupplayer'),
        ),
    ]
