# Generated by Django 4.1.1 on 2023-04-12 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_alter_coverletterdetails_coverletter'),
    ]

    operations = [
        migrations.AddField(
            model_name='interviewscheduling',
            name='job',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app1.jobdetails'),
        ),
    ]
