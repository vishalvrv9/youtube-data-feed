# Generated by Django 3.1.1 on 2020-09-24 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='video',
            index=models.Index(fields=['-published_at'], name='search_vide_publish_7fe4cd_idx'),
        ),
    ]