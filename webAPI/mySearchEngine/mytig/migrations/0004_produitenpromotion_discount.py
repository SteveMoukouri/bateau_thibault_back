# Generated by Django 3.1.7 on 2021-03-10 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytig', '0003_produitdisponible'),
    ]

    operations = [
        migrations.AddField(
            model_name='produitenpromotion',
            name='discount',
            field=models.FloatField(default=0),
        ),
    ]
