# Generated by Django 4.1 on 2024-07-27 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positive', models.IntegerField(default=0)),
                ('negative', models.IntegerField(default=0)),
                ('neutral', models.IntegerField(default=0)),
                ('confidence', models.FloatField(blank=True, default=None)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
            ],
        ),
    ]
