# Generated by Django 3.2.13 on 2023-11-07 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repositories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='description',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
    ]
