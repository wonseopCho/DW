# Generated by Django 2.0.3 on 2018-05-17 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0026_category_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='push_update',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listicle',
            name='push_update',
            field=models.BooleanField(default=False),
        ),
    ]
