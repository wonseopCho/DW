# Generated by Django 2.0.3 on 2018-04-13 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0011_auto_20180413_1357'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['parent', '-depth']},
        ),
    ]