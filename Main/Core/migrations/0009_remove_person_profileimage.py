# Generated by Django 2.1 on 2018-08-26 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0008_auto_20180826_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='profileImage',
        ),
    ]
