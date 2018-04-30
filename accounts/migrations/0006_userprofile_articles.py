# Generated by Django 2.0.3 on 2018-04-26 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0021_auto_20180426_1115'),
        ('accounts', '0005_auto_20180426_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='articles',
            field=models.ManyToManyField(related_name='user_articles', to='tips.Article'),
        ),
    ]