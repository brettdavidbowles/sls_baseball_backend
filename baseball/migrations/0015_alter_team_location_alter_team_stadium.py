# Generated by Django 4.1.5 on 2023-02-02 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseball', '0014_alter_player_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='location',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='stadium',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
