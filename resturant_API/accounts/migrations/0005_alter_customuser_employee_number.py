# Generated by Django 3.2 on 2022-04-11 20:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='employee_number',
            field=models.CharField(max_length=4, unique=True, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
    ]
