# Generated by Django 4.1 on 2024-07-28 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speechtool', '0002_entries_audio_file_entries_audio_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entries',
            name='confidence',
            field=models.FloatField(default=None, null=True),
        ),
    ]
