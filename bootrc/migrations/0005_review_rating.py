# Generated by Django 3.2.8 on 2021-11-17 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bootrc', '0004_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(default=0),
        ),
    ]