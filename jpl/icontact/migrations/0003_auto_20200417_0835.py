# Generated by Django 3.0.5 on 2020-04-17 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icontact', '0002_auto_20200417_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_name',
            field=models.CharField(max_length=50),
        ),
    ]
