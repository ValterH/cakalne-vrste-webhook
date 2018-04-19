# Generated by Django 2.0.3 on 2018-04-13 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0003_auto_20180412_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='procedure',
            name='groups',
            field=models.ManyToManyField(default=None, to='webhook.Group', verbose_name='list of groups'),
        ),
    ]