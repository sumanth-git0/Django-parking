# Generated by Django 5.0.7 on 2024-07-23 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parking_management', '0004_alter_parkhistory_fee_alter_parkhistory_in_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parkhistory',
            old_name='In',
            new_name='Intime',
        ),
        migrations.RenameField(
            model_name='parkhistory',
            old_name='Out',
            new_name='Outtime',
        ),
    ]
