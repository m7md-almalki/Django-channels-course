# Generated by Django 5.0.1 on 2024-02-13 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]
