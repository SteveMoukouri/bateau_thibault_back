# Generated by Django 3.1.7 on 2021-03-18 17:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myShop', '0005_auto_20210318_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='infosproduit',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
