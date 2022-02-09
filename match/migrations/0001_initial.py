# Generated by Django 4.0.1 on 2022-02-07 05:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_double', models.BooleanField(default=True)),
                ('player1_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player1_1', to=settings.AUTH_USER_MODEL)),
                ('player1_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player1_2', to=settings.AUTH_USER_MODEL)),
                ('player2_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player2_1', to=settings.AUTH_USER_MODEL)),
                ('player2_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player2_2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_has_seen', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_from', to=settings.AUTH_USER_MODEL)),
                ('match', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match', to='match.match')),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]