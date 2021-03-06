# Generated by Django 2.1.1 on 2018-09-18 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WxCredential',
            fields=[
                ('id', models.BigAutoField(db_column='ID', primary_key=True, serialize=False)),
                ('appid', models.CharField(max_length=100)),
                ('secret', models.CharField(max_length=100)),
                ('comment', models.CharField(default='', max_length=100)),
            ],
            options={
                'db_table': 'wx_credential',
            },
        ),
        migrations.CreateModel(
            name='WxToken',
            fields=[
                ('id', models.BigAutoField(db_column='ID', primary_key=True, serialize=False)),
                ('access_token', models.CharField(max_length=255)),
                ('expires_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'wx_token',
            },
        ),
    ]
