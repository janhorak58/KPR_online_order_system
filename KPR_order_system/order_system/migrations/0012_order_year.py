# Generated by Django 3.2.9 on 2021-11-24 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_system', '0011_order_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='year',
            field=models.IntegerField(default=2021),
        ),
    ]