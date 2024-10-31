# Generated by Django 4.2.3 on 2024-10-31 02:04

from django.db import migrations, models
import management.models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0007_alter_car_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.IntegerField(help_text='Insira apenas o ano.', null=True, validators=[management.models.validate_year]),
        ),
    ]
