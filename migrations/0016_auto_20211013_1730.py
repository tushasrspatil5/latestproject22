# Generated by Django 3.1.7 on 2021-10-13 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0015_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='long_desc1',
        ),
        migrations.RemoveField(
            model_name='product',
            name='long_desc2',
        ),
        migrations.RemoveField(
            model_name='product',
            name='long_desc3',
        ),
        migrations.RemoveField(
            model_name='product',
            name='long_desc4',
        ),
        migrations.RemoveField(
            model_name='product',
            name='long_desc5',
        ),
        migrations.AddField(
            model_name='product',
            name='benefits',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='product',
            name='desc',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='product',
            name='ingradients',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='product',
            name='manufacturer',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='safety_info',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='product',
            name='use',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='product',
            name='use_directions',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='sub_category',
            field=models.CharField(max_length=100),
        ),
    ]