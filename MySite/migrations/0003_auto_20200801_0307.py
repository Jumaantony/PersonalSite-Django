# Generated by Django 3.0.8 on 2020-08-01 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MySite', '0002_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
