# Generated by Django 3.2.20 on 2023-07-14 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20230714_1109'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='choice',
            new_name='answer',
        ),
    ]