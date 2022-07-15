# Generated by Django 4.0.4 on 2022-07-14 08:51

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommonInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commonInfoName', models.TextField()),
            ],
            options={
                'db_table': 'CommonInfo',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('builtYear', models.CharField(max_length=5, null=True)),
                ('commonInfo', models.JSONField(null=True)),
            ],
            options={
                'db_table': 'Room',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uId', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('uNickname', models.TextField()),
                ('uEmail', models.EmailField(max_length=254, unique=True)),
                ('uAccessToken', models.TextField(null=True)),
                ('uWarnCount', models.IntegerField(default=0)),
                ('uActive', models.IntegerField(default=0)),
                ('penaltyDate', models.DateField(default=datetime.date.today)),
            ],
            options={
                'db_table': 'user_info',
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('uId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='DBs.user')),
                ('mTel', models.TextField()),
            ],
            options={
                'db_table': 'manager',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewTitle', models.CharField(max_length=50)),
                ('reviewDate', models.DateField(default=datetime.date.today)),
                ('reviewKind', models.IntegerField()),
                ('reviewSentence', models.JSONField()),
                ('roomId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='whichRoom', to='DBs.room')),
                ('uId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='writer', to='DBs.user')),
            ],
            options={
                'db_table': 'Review',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportedOn', to='DBs.review')),
                ('uId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reporter', to='DBs.user')),
            ],
            options={
                'db_table': 'Report',
            },
        ),
        migrations.CreateModel(
            name='Recommend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendedOn', to='DBs.review')),
                ('uId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recommender', to='DBs.user')),
            ],
            options={
                'db_table': 'Recommend',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.TextField(null=True)),
                ('reviewId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additionalImage', to='DBs.review')),
            ],
            options={
                'db_table': 'Image',
            },
        ),
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iconKind', models.TextField()),
                ('changedIconKind', models.TextField()),
                ('iconInformation', models.TextField()),
                ('reviewId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='includedIcon', to='DBs.review')),
            ],
            options={
                'db_table': 'Icon',
            },
        ),
    ]