# Generated by Django 2.0.3 on 2018-04-26 02:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0020_comment_seq_in_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['group', 'seq_in_group']},
        ),
    ]
