# Generated by Django 4.2.5 on 2024-02-27 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0034_jobseekerprofile_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='experience',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
