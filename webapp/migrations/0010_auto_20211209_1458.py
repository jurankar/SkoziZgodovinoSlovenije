# Generated by Django 3.2.9 on 2021-12-09 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_auto_20211209_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Odgovor',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vprasanje',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AlterField(
            model_name='odgovorizberiodgovormodel',
            name='id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='webapp.odgovor'),
        ),
        migrations.AlterField(
            model_name='odgovoropisnomodel',
            name='id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='webapp.odgovor'),
        ),
        migrations.AlterField(
            model_name='odgovorpravilnonepravilnomodel',
            name='id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='webapp.odgovor'),
        ),
    ]
