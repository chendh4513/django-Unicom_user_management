# Generated by Django 4.1.2 on 2022-10-17 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_admin_alter_prettynum_moblie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='username',
            field=models.CharField(max_length=32, unique=True, verbose_name='用户名'),
        ),
        migrations.AlterField(
            model_name='department',
            name='title',
            field=models.CharField(max_length=32, unique=True, verbose_name='标题'),
        ),
    ]
