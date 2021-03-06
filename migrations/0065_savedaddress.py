# Generated by Django 3.2.6 on 2022-01-04 12:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0064_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('username', models.CharField(max_length=300)),
                ('landmark', models.CharField(max_length=1000)),
                ('room_no', models.CharField(max_length=1000)),
            ],
        ),
    ]
