# Generated by Django 4.2.7 on 2023-12-22 03:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogapp', '0011_alter_websitemeta_options_post_bookmarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
