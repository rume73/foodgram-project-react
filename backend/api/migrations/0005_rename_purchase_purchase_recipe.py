# Generated by Django 3.2.4 on 2021-09-13 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210913_0957'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='purchase',
            new_name='recipe',
        ),
    ]