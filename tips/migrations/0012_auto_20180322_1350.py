# Generated by Django 2.0.3 on 2018-03-22 04:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0011_auto_20180322_1348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='title',
        ),
        migrations.AddField(
            model_name='category',
            name='category',
            field=models.CharField(default=django.utils.timezone.now, max_length=20, primary_key=True, verbose_name='Category'),
            preserve_default=False,
        ),
    ]
