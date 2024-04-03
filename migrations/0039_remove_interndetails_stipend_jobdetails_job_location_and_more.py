# Generated by Django 4.2.5 on 2024-04-02 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0038_rename_skill_jobseekerprofile_skills_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interndetails',
            name='stipend',
        ),
        migrations.AddField(
            model_name='jobdetails',
            name='job_location',
            field=models.CharField(default='Some default value', max_length=500),
        ),
        migrations.AlterField(
            model_name='resumeschema',
            name='hssyear',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='resumeschema',
            name='passingyear',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='resumeschema',
            name='tenthpassyear',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
