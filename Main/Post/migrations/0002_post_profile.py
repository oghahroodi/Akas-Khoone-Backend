# Generated by Django 2.1 on 2018-09-05 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
        ('Post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='Profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Account.Person'),
            preserve_default=False,
        ),
    ]
