# Generated by Django 3.1.2 on 2020-12-13 09:01

from django.db import migrations
import mapbox_location_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorDetails', '0003_locationfiltermodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationfiltermodel',
            name='locationOfFilter',
            field=mapbox_location_field.models.LocationField(map_attrs={'id': 'unique_id_1'}),
        ),
    ]