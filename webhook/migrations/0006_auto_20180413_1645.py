# Generated by Django 2.0.3 on 2018-04-13 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0005_auto_20180413_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procedure',
            name='groups',
            field=models.ManyToManyField(default=None, to='webhook.Group', verbose_name='list of groups'),
        ),
    ]
