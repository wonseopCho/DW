# Generated by Django 2.0.7 on 2018-07-18 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qna', '0003_auto_20180717_1121'),
        ('accounts', '0015_auto_20180718_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='qna_cart',
            field=models.ManyToManyField(blank=True, related_name='user_cart_qna', to='qna.Qna'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='recommendation_cart',
            field=models.ManyToManyField(blank=True, related_name='user_cart_recommendation', to='recommendation.Recommendation'),
        ),
    ]
