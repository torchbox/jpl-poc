# Generated by Django 3.0.5 on 2020-04-15 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_newsindex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspage',
            name='introduction',
            field=models.TextField(blank=True, help_text='Use this field to give a brief intro to the news article.'),
        ),
    ]
