# Generated by Django 4.1.5 on 2023-02-01 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseball', '0007_alter_player_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='at_bats',
            field=models.ManyToManyField(blank=True, related_name='players', to='baseball.atbat'),
        ),
    ]
