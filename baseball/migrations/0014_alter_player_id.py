# Generated by Django 4.1.5 on 2023-02-01 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseball', '0013_alter_player_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]