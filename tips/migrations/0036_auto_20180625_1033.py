# Generated by Django 2.0.3 on 2018-06-25 01:33

from django.db import migrations
import sortedm2m.fields
from sortedm2m.operations import AlterSortedManyToManyField


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0035_auto_20180625_1032'),
    ]

    operations = [
        AlterSortedManyToManyField(
            model_name='listicle',
            name='articles',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='listicle_articles', to='tips.Article'),
        ),
    ]