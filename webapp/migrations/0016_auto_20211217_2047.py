# Generated by Django 3.2.9 on 2021-12-17 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0015_auto_20211217_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datotekaizberiodgovormodel',
            name='datoteka',
            field=models.FileField(upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='datotekaopisnomodel',
            name='datoteka',
            field=models.FileField(upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='datotekapravilnonepravilnomodel',
            name='datoteka',
            field=models.FileField(upload_to='media/'),
        ),
    ]
