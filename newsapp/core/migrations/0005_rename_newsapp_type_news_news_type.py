# Generated by Django 4.2.2 on 2023-08-02 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_news_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='newsapp_type',
            new_name='news_type',
        ),
    ]
