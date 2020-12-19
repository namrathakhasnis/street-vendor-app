from django.contrib import admin
from .models import VendorProfile, Category
# from mapbox_location_field.admin import MapAdmin


admin.site.register(VendorProfile)
admin.site.register(Category)
# admin.site.register(MapAdmin)