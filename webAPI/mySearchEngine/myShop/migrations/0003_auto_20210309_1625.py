# Generated by Django 3.1.7 on 2021-03-09 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myShop', '0002_auto_20210308_1710'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='infosproduit',
            options={'ordering': ('tigID', 'qtyInStock')},
        ),
        migrations.RemoveField(
            model_name='infosproduit',
            name='created',
        ),
        migrations.AddField(
            model_name='infosproduit',
            name='tigID',
            field=models.IntegerField(default='-1'),
        ),
    ]
