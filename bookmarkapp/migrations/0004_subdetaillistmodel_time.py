# Generated by Django 3.0 on 2020-05-16 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarkapp', '0003_auto_20200516_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='subdetaillistmodel',
            name='time',
            field=models.TimeField(default="11:11:11"),
            preserve_default=False,
        ),
    ]
