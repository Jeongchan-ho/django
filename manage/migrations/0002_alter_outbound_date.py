# Generated by Django 4.2 on 2023-04-07 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outbound',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
