# Generated by Django 4.2.5 on 2023-10-03 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_interviewscheduling_interviewlink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payementdetails',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='qualifications',
            name='cmp_id',
        ),
        migrations.RemoveField(
            model_name='skills',
            name='emp_profile',
        ),
        migrations.RemoveField(
            model_name='jobdetails',
            name='qualification',
        ),
        migrations.RemoveField(
            model_name='jobseekerprofile',
            name='highestqualification',
        ),
        migrations.RemoveField(
            model_name='verificationdetails',
            name='proof',
        ),
        migrations.RemoveField(
            model_name='verificationdetails',
            name='proof_type',
        ),
        migrations.DeleteModel(
            name='CoverLetterDetails',
        ),
        migrations.DeleteModel(
            name='PayementDetails',
        ),
        migrations.DeleteModel(
            name='Qualifications',
        ),
        migrations.DeleteModel(
            name='Skills',
        ),
    ]
