# Generated by Django 3.1.7 on 2021-11-16 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0055_auto_20211115_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='razorpay_order_id',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
