# Generated by Django 3.0.7 on 2020-06-06 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20200605_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fleet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fleet_id', models.CharField(max_length=20)),
                ('ids', models.CharField(max_length=300)),
            ],
        ),
    ]