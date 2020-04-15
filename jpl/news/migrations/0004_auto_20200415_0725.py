# Generated by Django 3.0.5 on 2020-04-15 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
        ('news', '0003_auto_20200415_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspage',
            name='hero_banner',
            field=models.ForeignKey(blank=True, help_text='Image used for the banner and thumbnail on the index page.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.CustomImage'),
        ),
    ]
