# Generated by Django 3.1.2 on 2020-12-13 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorDetails', '0004_auto_20201213_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationfiltermodel',
            name='locFilterAddress',
            field=models.CharField(default=None, max_length=2000000, null=True),
        ),
    ]