# Generated by Django 2.0.1 on 2018-02-07 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog2', '0007_auto_20180207_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
