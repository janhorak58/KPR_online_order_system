# Generated by Django 3.2.9 on 2021-11-22 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_system', '0003_alter_order_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='posta',
        ),
    ]