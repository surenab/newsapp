# Generated by Django 4.2.4 on 2023-09-10 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_remove_newscomment_date_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]