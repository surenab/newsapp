# Generated by Django 4.2.2 on 2023-08-07 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_article_rename_photos_team_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]