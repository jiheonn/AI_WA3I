# Generated by Django 3.0.6 on 2020-06-11 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='makequestion',
            name='upload_check',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
