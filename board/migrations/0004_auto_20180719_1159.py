# Generated by Django 2.0.7 on 2018-07-19 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_auto_20180719_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='b_title',
            field=models.CharField(max_length=100),
        ),
    ]
