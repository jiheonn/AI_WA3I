# Generated by Django 3.0.6 on 2020-06-17 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0002_auto_20200611_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='makequestion',
            name='image',
            field=models.ImageField(upload_to='makequestion/image'),
        ),
    ]