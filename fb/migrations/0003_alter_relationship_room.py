# Generated by Django 3.2.4 on 2021-07-11 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb', '0002_alter_relationship_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationship',
            name='room',
            field=models.CharField(default='ezvhkorh', max_length=8),
        ),
    ]
