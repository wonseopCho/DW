# Generated by Django 2.0.3 on 2018-06-18 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0004_auto_20180618_1232'),
        ('accounts', '0012_userprofile_article_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='recommendation_cart',
            field=models.ManyToManyField(blank=True, related_name='user_recommendation', to='recommendation.Recommendation'),
        ),
    ]
