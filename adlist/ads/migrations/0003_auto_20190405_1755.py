# Generated by Django 2.1.5 on 2019-04-05 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_auto_20190402_2026'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ad',
            old_name='ads',
            new_name='owner',
        ),
    ]
