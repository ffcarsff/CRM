# Generated by Django 4.2.1 on 2023-06-06 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0006_alter_worker_phonned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='phonned',
            field=models.BooleanField(default=False),
        ),
    ]