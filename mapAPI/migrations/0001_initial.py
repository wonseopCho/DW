# Generated by Django 2.0.3 on 2018-03-23 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MapAddress',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('address', models.CharField(max_length=80)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lng', models.FloatField(blank=True, null=True)),
                ('type', models.CharField(max_length=30)),
            ],
        ),
    ]
