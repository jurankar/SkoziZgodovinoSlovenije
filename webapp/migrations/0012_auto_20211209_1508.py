# Generated by Django 3.2.9 on 2021-12-09 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0011_auto_20211209_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='izberiodgovormodel',
            name='id',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='opisnomodel',
            name='id',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='pravilnonepravilnomodel',
            name='id',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
    ]
