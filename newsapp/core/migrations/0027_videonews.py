# Generated by Django 4.2.2 on 2023-09-21 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_delete_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('video_url', models.URLField()),
                ('description', models.TextField()),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]