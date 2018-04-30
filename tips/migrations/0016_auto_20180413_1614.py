# Generated by Django 2.0.3 on 2018-04-13 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0015_auto_20180413_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent_writer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_writer', to=settings.AUTH_USER_MODEL),
        ),
    ]