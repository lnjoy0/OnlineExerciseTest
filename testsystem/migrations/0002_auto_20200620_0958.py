# Generated by Django 3.0.7 on 2020-06-20 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsystem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=256, verbose_name='密码'),
        ),
    ]