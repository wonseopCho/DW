# Generated by Django 2.0.3 on 2018-04-12 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0007_auto_20180410_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='depth',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
