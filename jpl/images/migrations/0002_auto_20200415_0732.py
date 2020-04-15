# Generated by Django 3.0.5 on 2020-04-15 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customimage',
            name='caption',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='customimage',
            name='alt',
            field=models.CharField(blank=True, max_length=255, verbose_name='Alt text'),
        ),
    ]