# Generated by Django 2.1 on 2018-08-26 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0002_auto_20180825_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='date',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
    ]
