# Generated by Django 2.0.7 on 2018-07-19 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20180719_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.FileField(upload_to='board/images/%Y/%m/%d'),
        ),
    ]
