# Generated by Django 4.1.1 on 2023-04-03 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interviewscheduling',
            name='status',
            field=models.BooleanField(default=0, verbose_name='status'),
        ),
    ]
