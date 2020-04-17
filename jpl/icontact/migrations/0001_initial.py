# Generated by Django 3.0.5 on 2020-04-17 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign_id', models.PositiveIntegerField()),
                ('message_name', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('html_body', models.TextField()),
                ('text_body', models.TextField()),
                ('source_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page')),
            ],
        ),
    ]
