# Generated by Django 2.1 on 2018-09-07 11:32

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


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
                ('name', models.CharField(max_length=100)),
                ('bio', models.CharField(max_length=250, null=True)),
                ('followerNumber', models.IntegerField(default=0)),
                ('followingNumber', models.IntegerField(default=0)),
                ('phoneNumber', models.CharField(blank=True, max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('validation', models.BooleanField(default=False)),
                ('accountCreationDate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('username', models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(message='Username can only contain numbers,charachters, _ and .', regex='^[a-zA-Z0-9_.]*$')])),
                ('postNumber', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userFollowed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed', to=settings.AUTH_USER_MODEL)),
                ('userFollowing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
