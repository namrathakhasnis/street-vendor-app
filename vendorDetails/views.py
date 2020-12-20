from django.shortcuts import render, get_object_or_404
from .models import VendorProfile, Category
from django.utils import timezone
from .forms import VendorForm,LocationFilterForm
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from functools import reduce
import operator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

def post_list(request):
    profiles = VendorProfile.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    categories = Category.objects.all()
    if categories.count()==0:
        newCatVeg= Category(category_name='Vegetables and Fruits', category_description='Find the best vegetable and fruits vendors')
        newCatVeg.save()
        newCatFood=Category(category_name='Food', category_description='Craving street food? Find the best ones near you')
        newCatFood.save()
        newCatClothes=Category(category_name='Jewelery', category_description='Find the best of traditional jewelery near you!')
        newCatClothes.save()
        newCatJewelry=Category(category_name='Clothes', category_description='Looking for some dapper clothes? Find them over here!')
        newCatJewelry.save()
        newCatArtiFacts=Category(category_name='Articrafts, Home-Decor and Kitchen', category_description='The tradition of India to style your living!')
        newCatArtiFacts.save()
        newCatBooks=Category(category_name='Books', category_description='Evoke the reader within you!')
        newCatBooks.save()
    categories = Category.objects.all()
    print(categories)
    profile_with_cat_dict= {}
    for cat in categories:
        profile_with_cat_dict[int(cat.id)]=cat.profiles.all()
    print(profile_with_cat_dict)
    if request.user.is_authenticated:
        if request.method == "POST":
            if 'bannedphrase' in request.POST:
                bannedphraseform = LocationFilterForm(request.POST)
                locSelected= bannedphraseform.save(commit=False)
                profile_with_cat_dict = {}
                qList= locSelected.locFilterAddress.split()
                query = reduce(operator.or_, (Q(addressloc__contains=item) for item in qList))
                for cat in categories:
                    profile_with_cat_dict[int(cat.id)]=cat.profiles.filter(query)
                form = VendorForm()
                locForm = LocationFilterForm()
            else:
                form = VendorForm(request.POST, request.FILES)
                if form.is_valid():
                    post = form.save(commit=False)
                    selected_item = get_object_or_404(Category, pk=request.POST.get('category_id'))
                    post.categoryId = selected_item
                    post.creator = request.user
                    post.created_date = timezone.now()
                    post.save()
                    return redirect('post_detail', pk=post.pk)
        else:
            form = VendorForm()
            locForm=LocationFilterForm()
    else:
            form=None
            locForm=None
    return render(request, 'vendorDetails/index.html', {'profiles': profile_with_cat_dict, 'form': form, 'categories': categories, 'locForm': locForm})
def post_detail(request, pk):
    post = get_object_or_404(VendorProfile, pk=pk)
    return render(request, 'vendorDetails/post_detail.html', {'post': post})
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print("form crwated")
        if form.is_valid():
            form.save()
            print('form saved')
            username = form.cleaned_data.get('username')
            print(username)
            raw_password = form.cleaned_data.get('password1')
            print(raw_password)
            user = authenticate(username=username, password=raw_password)
            print(user)
            login(request, user)
            print("logged in")
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'vendorDetails/signup.html', {'form': form})