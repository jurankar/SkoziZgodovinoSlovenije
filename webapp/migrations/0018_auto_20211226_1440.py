# Generated by Django 3.2.9 on 2021-12-26 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0017_auto_20211219_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='izberiodgovormodel',
            name='leto',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='opisnomodel',
            name='leto',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pravilnonepravilnomodel',
            name='leto',
            field=models.IntegerField(default=0),
        ),
    ]
