# Generated by Django 2.1 on 2019-07-25 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservideomapping',
            name='user_id',
            field=models.IntegerField(),
        ),
    ]
