# Generated by Django 3.2.9 on 2021-11-24 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_system', '0010_auto_20211124_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='month',
            field=models.IntegerField(default=11),
        ),
    ]
