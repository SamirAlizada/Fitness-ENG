# Generated by Django 4.1.2 on 2024-07-04 15:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0012_dailypricing_student_daily'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]