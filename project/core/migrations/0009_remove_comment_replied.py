# Generated by Django 5.0.1 on 2024-01-31 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_comment_replied'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='replied',
        ),
    ]