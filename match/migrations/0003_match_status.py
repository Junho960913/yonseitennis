# Generated by Django 4.0.1 on 2022-02-07 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0002_match_games_match_sets'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='status',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
