# Generated by Django 3.2.9 on 2021-12-09 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_auto_20211209_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='odgovorizberiodgovormodel',
            name='id',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='odgovoropisnomodel',
            name='id',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='odgovorpravilnonepravilnomodel',
            name='id',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
    ]
