# Generated by Django 2.0.3 on 2018-04-23 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180423_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='photo_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
