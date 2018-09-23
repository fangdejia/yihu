# Generated by Django 2.1.1 on 2018-09-22 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxapi', '0002_wxtoken_wx_credential'),
    ]

    operations = [
        migrations.CreateModel(
            name='WxSession',
            fields=[
                ('id', models.BigAutoField(db_column='ID', primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=36)),
                ('session_key', models.CharField(max_length=30)),
                ('open_id', models.CharField(max_length=28)),
                ('union_id', models.CharField(max_length=29)),
            ],
            options={
                'db_table': 'wx_session',
            },
        ),
    ]
