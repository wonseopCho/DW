# Generated by Django 2.0.3 on 2018-06-18 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20180618_1539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='recommendation_cart',
        ),
    ]