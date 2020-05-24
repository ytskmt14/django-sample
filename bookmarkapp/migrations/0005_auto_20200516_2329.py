# Generated by Django 3.0 on 2020-05-16 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarkapp', '0004_subdetaillistmodel_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subdetaillistmodel',
            name='top_id',
        ),
        migrations.AlterField(
            model_name='detaillistmodel',
            name='top_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmarkapp.TopListModel'),
        ),
        migrations.AlterField(
            model_name='subdetaillistmodel',
            name='detail_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookmarkapp.DetailListModel'),
        ),
    ]
