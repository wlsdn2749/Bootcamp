# Generated by Django 3.2.8 on 2021-10-31 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bootrc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restmenu',
            name='rest_num',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bootrc.rest'),
        ),
    ]