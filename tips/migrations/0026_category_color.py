# Generated by Django 2.0.3 on 2018-05-09 06:46

import colorful.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0025_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=colorful.fields.RGBColorField(default=''),
            preserve_default=False,
        ),
    ]