# Generated by Django 3.0 on 2020-06-07 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarkapp', '0003_auto_20200605_0750'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailWork',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('main_content', models.CharField(max_length=100)),
            ],
        ),
    ]
