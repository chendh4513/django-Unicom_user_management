# Generated by Django 4.1.2 on 2022-10-17 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='username',
            field=models.CharField(max_length=32, verbose_name='用户名'),
        ),
    ]
