# Generated by Django 4.1.2 on 2024-07-08 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0013_bar_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tariffs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('type', models.CharField(choices=[('daily', 'Daily'), ('monthly', 'Monthly')], max_length=10)),
                ('month_duration', models.IntegerField(blank=True, null=True)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='student',
            name='daily',
        ),
        migrations.RemoveField(
            model_name='student',
            name='months_duration',
        ),
        migrations.DeleteModel(
            name='DailyPricing',
        ),
        migrations.DeleteModel(
            name='MonthlyPricing',
        ),
        migrations.AddField(
            model_name='student',
            name='tariffs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fitness.tariffs'),
        ),
    ]
