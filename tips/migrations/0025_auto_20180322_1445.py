# Generated by Django 2.0.3 on 2018-03-22 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0024_category_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Title'),
        ),
    ]
