# Generated by Django 4.2.5 on 2024-01-28 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0017_question_feedback_choice'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
