# Generated by Django 4.0.6 on 2022-07-22 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0003_rename_note_id_note_note_id_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='note_id_id',
            new_name='user_id',
        ),
    ]
