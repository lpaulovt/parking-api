# Generated by Django 4.2.3 on 2024-10-30 23:58

from django.db import migrations, models
import management.models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_alter_car_license_plate_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='year',
            field=models.IntegerField(default=2000, help_text='Insira apenas o ano (ex: 2024).', validators=[management.models.validate_year]),
            preserve_default=False,
        ),
    ]