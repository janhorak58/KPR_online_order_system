# Generated by Django 3.2.9 on 2021-11-21 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_system', '0002_auto_20211121_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]