# Generated by Django 3.1.3 on 2020-12-08 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('datetime', models.DateTimeField(primary_key=True, serialize=False)),
                ('temperature_value', models.CharField(max_length=20)),
            ],
        ),
    ]