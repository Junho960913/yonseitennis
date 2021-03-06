# Generated by Django 4.0.1 on 2022-02-07 02:49

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=24)),
                ('nickname', models.CharField(max_length=24, unique=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('points', models.IntegerField(default=0)),
                ('rank', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'User',
            },
            managers=[
                ('objects', user.models.UserManager()),
            ],
        ),
    ]
