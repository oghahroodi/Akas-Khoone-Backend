# Generated by Django 2.1 on 2018-09-11 11:03

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
            name='ForgetPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('code', models.CharField(max_length=11)),
                ('accepted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bio', models.CharField(max_length=250, null=True)),
                ('followerNumber', models.IntegerField(default=0)),
                ('followingNumber', models.IntegerField(default=0)),
                ('phoneNumber', models.CharField(blank=True, max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message='شماره تلفن باید عدد و بین 9 تا 15 رقم باشد.', regex='^\\+?1?\\d{9,15}$')])),
                ('validation', models.BooleanField(default=False)),
                ('accountCreationDate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('username', models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(message='نام کاربری فقط شامل حروف انگلیسی، عدد، _ و . است.', regex='^[a-zA-Z0-9_.]*$')])),
                ('postNumber', models.IntegerField(default=0)),
                ('boardNumber', models.IntegerField(default=0)),
                ('profileImage', models.ImageField(upload_to='images/%Y/%m/%d/')),
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
