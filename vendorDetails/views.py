from django.shortcuts import render
from .models import VendorProfile
from django.utils import timezone
# Create your views here.

def post_list(request):
    profiles=VendorProfile.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'vendorDetails/post_list.html', {'profiles': profiles})
