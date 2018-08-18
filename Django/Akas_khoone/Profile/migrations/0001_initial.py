# Generated by Django 2.1 on 2018-08-18 09:44

import Profile.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Bio', models.CharField(max_length=250, null=True)),
                ('FollowerNumber', models.IntegerField(default=0)),
                ('FollowingNumber', models.IntegerField(default=0)),
                ('PhoneNumber', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('validation', models.BooleanField(default=False)),
                ('AcountCreationDate', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Pic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PicAdress', models.ImageField(upload_to=Profile.models.user_directory_path)),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='pic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Profile.Pic'),
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
