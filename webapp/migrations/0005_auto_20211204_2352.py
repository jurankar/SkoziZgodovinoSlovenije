# Generated by Django 3.2.9 on 2021-12-04 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_rename_dbkviz_dbquiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dbanswer',
            name='vprasanje',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='dbquestion',
            name='kviz',
            field=models.CharField(max_length=100),
        ),
    ]
