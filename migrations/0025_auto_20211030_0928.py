# Generated by Django 3.1.7 on 2021-10-30 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0024_shop_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='personaldetails',
            name='lat',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personaldetails',
            name='lon',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
