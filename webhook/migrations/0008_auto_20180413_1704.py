# Generated by Django 2.0.3 on 2018-04-13 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0007_auto_20180413_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='procedures',
            field=models.ManyToManyField(blank=True, to='webhook.Procedure', verbose_name='list of procedures'),
        ),
    ]