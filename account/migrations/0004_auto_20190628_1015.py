# Generated by Django 2.2.1 on 2019-06-28 02:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_userinfo_phono'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='phono',
            new_name='photo',
        ),
    ]
