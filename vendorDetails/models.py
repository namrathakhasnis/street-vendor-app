from django.conf import settings
from django.db import models
from django.utils import timezone


class VendorProfile(models.Model):
   # category = models.ForeignKey(settings.CATEGORY, on_delete=models.CASCADE)
    vendorName = models.CharField(max_length=200)
    description = models.TextField()
    phoneNumber = models.CharField(max_length=20)
    age = models.CharField(max_length=2)
    #vendorType = models.ForeignKey(settings.VENDOR_TYPE, on_delete=models.CASCADE)
    #availability = models.ForeignKey(settings.AVAILABILITY, on_delete=models.CASCADE)
    #city = models.ForeignKey(settings.CITY, on_delete=models.CASCADE)
    creator=  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.vendorName
