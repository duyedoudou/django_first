# Generated by Django 2.2.1 on 2019-08-10 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20190810_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
