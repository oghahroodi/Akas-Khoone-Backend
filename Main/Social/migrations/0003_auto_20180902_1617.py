# Generated by Django 2.1 on 2018-09-02 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Social', '0002_auto_20180902_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='headComment',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Social.Comment'),
        ),
    ]
