# Generated by Django 3.2.4 on 2021-06-27 09:02

from django.conf import settings
from django.db import migrations, models
import fb.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fb', '0006_auto_20210626_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cover_photo',
            field=models.ImageField(upload_to=fb.models.cover_photo_upload),
        ),
        migrations.AlterField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(upload_to=fb.models.profile_photo_upload),
        ),
    ]
