# Generated by Django 3.2.9 on 2021-12-04 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_kviz_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Odgovor',
            new_name='dbAnswer',
        ),
        migrations.RenameModel(
            old_name='Kviz',
            new_name='dbKviz',
        ),
        migrations.RenameModel(
            old_name='Question',
            new_name='dbQuestion',
        ),
    ]
