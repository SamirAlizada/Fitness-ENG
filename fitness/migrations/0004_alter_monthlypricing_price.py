# Generated by Django 4.1.2 on 2024-04-21 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0003_bar_alter_trainer_monthly_fee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlypricing',
            name='price',
            field=models.IntegerField(),
        ),
    ]
