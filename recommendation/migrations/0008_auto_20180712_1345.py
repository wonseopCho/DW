# Generated by Django 2.0.3 on 2018-07-12 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0007_auto_20180712_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='contact',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='information',
            field=models.TextField(blank=True, null=True),
        ),
    ]