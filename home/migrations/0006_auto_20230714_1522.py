# Generated by Django 3.2.20 on 2023-07-14 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_rename_choice_user_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
    ]
