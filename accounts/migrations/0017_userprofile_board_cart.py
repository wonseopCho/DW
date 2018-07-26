# Generated by Django 2.0.7 on 2018-07-19 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_auto_20180719_1159'),
        ('accounts', '0016_auto_20180718_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='board_cart',
            field=models.ManyToManyField(blank=True, related_name='user_cart_qna', to='board.Board'),
        ),
    ]