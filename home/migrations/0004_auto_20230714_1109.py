# Generated by Django 3.2.20 on 2023-07-14 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20230714_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='choice',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
