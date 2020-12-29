from django import forms

from .models import VendorProfile,LocationFilterModel


class VendorForm(forms.ModelForm):

    class Meta:
        model = VendorProfile
        fields = ('vendorName', 'description', 'phoneNumber', 'age', 'vendorImg','location','addressloc', 'zipcodeLoc',)
class LocationFilterForm(forms.ModelForm):
    class Meta:
        model=LocationFilterModel
        fields=('locationOfFilter','locFilterAddress','locFilterZipcodeLoc')