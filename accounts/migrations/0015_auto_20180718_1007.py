# Generated by Django 2.0.7 on 2018-07-18 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20180712_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='article_cart',
            field=models.ManyToManyField(blank=True, related_name='user_cart_articles', to='tips.Article'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='recommendation_cart',
            field=models.ManyToManyField(blank=True, related_name='user_cart_qna', to='qna.Qna'),
        ),
    ]
