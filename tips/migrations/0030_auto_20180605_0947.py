# Generated by Django 2.0.3 on 2018-06-05 00:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0029_auto_20180605_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]
