# Generated by Django 4.2.5 on 2024-02-23 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0026_skill_remove_jobseekerprofile_skill_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobseekerprofile',
            name='skills',
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
    ]
