# Generated by Django 2.0.3 on 2018-04-10 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0004_auto_20180410_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='articles_listicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articles', models.ManyToManyField(related_name='articles_listicle', to='tips.Article')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tips.Category')),
            ],
        ),
        migrations.AlterField(
            model_name='listicle',
            name='articles',
            field=models.ManyToManyField(related_name='listicle_articles', to='tips.Article'),
        ),
    ]
