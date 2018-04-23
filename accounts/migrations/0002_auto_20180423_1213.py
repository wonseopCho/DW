# Generated by Django 2.0.3 on 2018-04-23 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='locale',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='accounts/user_profile/%Y/%m/%d'),
        ),
    ]
