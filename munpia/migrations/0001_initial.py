# Generated by Django 3.0.3 on 2020-05-22 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TodayBest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('genre', models.CharField(max_length=10)),
                ('author', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=50)),
                ('intro', models.TextField()),
            ],
        ),
    ]
