# Generated by Django 3.2.9 on 2021-11-22 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_system', '0004_remove_address_posta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]