# Generated by Django 2.0.3 on 2018-07-11 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0036_auto_20180625_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='find_keyword',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
