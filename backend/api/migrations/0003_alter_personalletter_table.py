# Generated by Django 5.0.4 on 2024-05-14 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_personalletter_email_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='personalletter',
            table='letter_creator',
        ),
    ]
