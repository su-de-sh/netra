# Generated by Django 3.0.7 on 2020-06-05 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20200605_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='gps',
            name='altitude',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='gps',
            name='temperature',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True),
        ),
    ]