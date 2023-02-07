# Generated by Django 4.1.5 on 2023-02-07 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseball', '0021_atbat_game_at_bat_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leftonrunner',
            name='at_bat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='runners_left_on_base', to='baseball.atbat'),
        ),
    ]