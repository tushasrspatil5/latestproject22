# Generated by Django 3.1.7 on 2021-11-09 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0039_orders_store_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='billimage_store',
        ),
        migrations.AddField(
            model_name='orders',
            name='bill_img_id',
            field=models.CharField(default='', max_length=200),
        ),
    ]