# Generated by Django 3.0.3 on 2020-05-24 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tocsoda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='web_best',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('genre', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=50)),
                ('intro', models.TextField()),
            ],
        ),
        migrations.RenameModel(
            old_name='TodayBest',
            new_name='free_best',
        ),
    ]