# Generated by Django 3.1.7 on 2021-10-01 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('lat', models.CharField(max_length=500)),
                ('lan', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=1000)),
                ('city', models.CharField(max_length=1000)),
            ],
        ),
    ]
