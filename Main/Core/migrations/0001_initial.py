# Generated by Django 2.1 on 2018-08-19 13:16

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
                ('name', models.CharField(max_length=100)),
                ('bio', models.CharField(max_length=250, null=True)),
                ('followerNumber', models.IntegerField(default=0)),
                ('followingNumber', models.IntegerField(default=0)),
                ('phoneNumber', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('validation', models.BooleanField(default=False)),
                ('acountCreationDate', models.DateTimeField(verbose_name='date published')),
                ('username', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PicPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PicAdress', models.ImageField(upload_to='')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.Person')),
            ],
        ),
        migrations.CreateModel(
            name='PicPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picAdress', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250, null=True)),
                ('likeNumber', models.IntegerField(default=0)),
                ('commetNumber', models.IntegerField(default=0)),
                ('date', models.DateTimeField(verbose_name='date published')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.Person')),
            ],
        ),
        migrations.AddField(
            model_name='picpost',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.Post'),
        ),
    ]