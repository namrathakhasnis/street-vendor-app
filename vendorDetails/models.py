from django.conf import settings
from django.db import models
from django.utils import timezone
from mapbox_location_field.models import LocationField, AddressAutoHiddenField


class VendorProfile(models.Model):
    vendorName = models.CharField(verbose_name='Vendor Name', max_length=200)
    description = models.TextField(verbose_name='Description')
    phoneNumber = models.CharField(verbose_name='Phone Number',  max_length=20,blank=True, null=True)
    age = models.CharField(verbose_name='Age', max_length=2,blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,  null=True, default=None, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    vendorImg = models.ImageField(verbose_name="A picture of the vendor:", upload_to='upload/',null=True, default=None)
    categoryId = models.ForeignKey('vendorDetails.Category', verbose_name="What category of items does this vendor sell?", on_delete=models.CASCADE, related_name='profiles', default=None )
    location = LocationField()
    addressloc = models.CharField(max_length=2000000)
    zipcodeLoc= models.CharField(max_length=100)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.vendorName

class Category(models.Model):
    category_name= models.CharField(max_length=500)
    category_description= models.CharField(max_length=200)

class LocationFilterModel(models.Model):
    locationOfFilter=LocationField(map_attrs={"id": "unique_id_1"})
    locFilterAddress= models.CharField(max_length=2000000,null=True, default=None)
    locFilterZipcodeLoc = models.CharField(max_length=100,null=True, default="")
