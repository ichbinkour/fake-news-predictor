# Generated by Django 2.2.3 on 2020-03-01 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleExemple',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_text', models.TextField()),
                ('medbias_score', models.FloatField()),
                ('medbias_class', models.IntegerField()),
                ('q_score', models.FloatField()),
                ('q_class', models.IntegerField()),
                ('origin_url', models.TextField()),
                ('origin_source', models.TextField()),
            ],
        ),
    ]
