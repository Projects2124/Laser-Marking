# Generated by Django 5.0.2 on 2024-03-06 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RPA', '0005_alter_running_part_tbl_selected_part'),
    ]

    operations = [
        migrations.RenameField(
            model_name='running_part_tbl',
            old_name='selected_part',
            new_name='Part_Name',
        ),
    ]
