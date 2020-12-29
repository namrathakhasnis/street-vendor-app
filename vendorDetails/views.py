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
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
import six
import plotly
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.ticker import MaxNLocator
import numpy as np
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
    profile_with_cat_dict= {}
    for cat in categories:
        profile_with_cat_dict[int(cat.id)]=cat.profiles.all()
    if request.user.is_authenticated:
        if request.method == "POST":
            if 'bannedphrase' in request.POST:
                bannedphraseform = LocationFilterForm(request.POST)
                locSelected= bannedphraseform.save(commit=False)
                profile_with_cat_dict = {}
                qList= str(locSelected.locFilterZipcodeLoc)
                for cat in categories:
                    profile_with_cat_dict[int(cat.id)]=cat.profiles.filter(Q(addressloc__icontains=qList) | Q(zipcodeLoc__icontains=qList))
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

def getAnalytics(request):
    profiles = VendorProfile.objects.order_by('created_date').values()
    df= pd.DataFrame({
            'Date_of_entry': [val['created_date'].date() for val in profiles],
            'Locality': [val['zipcodeLoc'] for val in profiles],
            'Category': [  get_object_or_404(Category, pk=val['categoryId_id']).category_name for val in profiles ],
            'Vendor_Name':[val['vendorName'] for val in profiles]
    })
    getBarGraphAnalytics(df)
    getScatterPlot(profiles)
    getPlotForLocalityAndNumber(df)
    aStateAndCategoryRepresentation=df.groupby(["Locality", "Category"], as_index=False)["Vendor_Name"].count()
    aStateAndCategoryRepresentation.columns.values[2]='Number of Vendors'
    aStateAndCategoryRepresentation.loc[df.duplicated('Locality') , 'Locality'] = ''
    htmlTable=getTableAsHeatMap(aStateAndCategoryRepresentation)

    return render(request, 'vendorDetails/getAnalytics.html', {'imgOfTable': htmlTable})

def getPlotForLocalityAndNumber(df):
    n_by_state = df.groupby(["Locality"], as_index=False)["Vendor_Name"].count()
    n_by_state.columns.values[1] = 'Number_of_Vendors'
    print(n_by_state)
    plt.clf()
    plt.plot(n_by_state.Locality, n_by_state.Number_of_Vendors)
    plt.xlabel("Locality")
    plt.ylabel("Number of Vendors")
    plt.tight_layout()
    plt.savefig("vendorDetails/static/outputPlotForLocVsNo.png")

def getBarGraphAnalytics(df):
    newColsByStateForPlot = df.groupby(["Locality", "Category"])["Vendor_Name"].count()
    dfForPlot = newColsByStateForPlot.unstack(level=-1)
    dfForPlot.fillna(value=0, inplace=True)
    dfForPlot.replace(np.nan, 0)
    print(dfForPlot)
    fig = dfForPlot.plot(kind="bar", figsize=(9, 6)).get_figure()
    #plt.yticks([])
    plt.tight_layout()
    fig.savefig("vendorDetails/static/outputMap.png")
def getScatterPlot(profiles):
    df = pd.DataFrame({
        'Date_of_entry': [val['created_date'].date() for val in profiles],
        'Locality': [val['zipcodeLoc'] for val in profiles],
        'Category': [  get_object_or_404(Category, pk=val['categoryId_id']).category_name for val in profiles ],
        'Vendor_Name': [val['vendorName'] for val in profiles]
    })
    n_by_state = df.groupby(["Locality", "Category"], as_index=False)["Vendor_Name"].count()
    n_by_state.columns.values[2] = 'Number_of_Vendors'
    cond = n_by_state.Category == 'Jewelery'
    cond2= n_by_state.Category== 'Articrafts, Home-Decor and Kitchen'
    cond3= n_by_state.Category == 'Vegetables and Fruits'
    cond4= n_by_state.Category == 'Food'
    cond5 = n_by_state.Category== 'Books'
    cond6 = n_by_state.Category =='Clothes'
    subset_a = n_by_state[cond]
    subset_b = n_by_state[cond2]
    subset_c = n_by_state[cond3]
    subset_d = n_by_state[cond4]
    subset_e= n_by_state[cond5]
    subset_f= n_by_state[cond6]
    print(n_by_state)
    plt.clf()
    plt.scatter(subset_a.Locality, subset_a.Number_of_Vendors,  c='#e91e63', label='Category= Jewelery')
    plt.scatter(subset_b.Locality, subset_b.Number_of_Vendors, c='brown', label='Category= Articrafts, Home-Decor and Kitchen')
    plt.scatter(subset_c.Locality, subset_c.Number_of_Vendors,  c='green', label='Category= Vegetables and Fruits')
    plt.scatter(subset_d.Locality, subset_d.Number_of_Vendors,  c='orange', label='Category= Food')
    plt.scatter(subset_e.Locality, subset_e.Number_of_Vendors,  c='blue', label='Category= Books')
    plt.scatter(subset_f.Locality, subset_f.Number_of_Vendors,  c='black', label='Category= Clothes')
    plt.legend()
    plt.xlabel("Locality")
    plt.ylabel("Number of Vendors")
    #plt.yticks([])
    plt.tight_layout()
    plt.savefig("vendorDetails/static/outputScatterMap.png")

def SaveTableAsImage(aStateAndCategoryRepresentation, df):
    size = (np.array(aStateAndCategoryRepresentation.shape[::-1]) + np.array([0, 1])) * np.array([3.0, 0.625])
    fig, ax = plt.subplots(figsize=size)
    ax.axis('off')
    ax.axis([0, 1, aStateAndCategoryRepresentation.shape[0], -1])
    mpl_table = table(ax, aStateAndCategoryRepresentation, rowLabels=[''] * df.shape[0], loc='center',
                      bbox=[0, 0, 1, 1])
    mpl_table.set_fontsize(16)
    row_colors = ['#f1f1f2', 'w']

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor('w')
        if k[0] == 0 or k[1] < 0:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor('#40466e')
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])
    plt.savefig('mytable.png')

def getTableAsHeatMap(df):
    styled_df=df.style.set_table_styles([{'selector': 'th', 'props': [('font-size', '20pt')]}]).set_properties(**{
    'font-size': '20pt',
}).background_gradient(cmap='Reds').applymap(color_negative_red, subset=['Category',]).apply(hightlight_price, axis=1)
    return  styled_df.render()

def color_negative_red(value):
  if value == 'Jewelery':
    color = '#e91e63'
  elif value == 'Articrafts, Home-Decor and Kitchen':
    color = 'brown'
  elif value == 'Vegetables and Fruits':
    color = 'green'
  elif value == 'Food':
    color = 'orange'
  elif value == 'Books':
    color = 'blue'
  else:
    color = 'black'

  return 'color: %s !important' % color

def hightlight_price(row):
    ret = ["" for _ in row.index]
    if row.Category == 'Jewelery':
        ret[row.index.get_loc("Number of Vendors")] = "color: #e91e63"
    elif row.Category == 'Articrafts, Home-Decor and Kitchen':
        ret[row.index.get_loc("Number of Vendors")] = "color: brown"
    elif row.Category == 'Vegetables and Fruits':
        ret[row.index.get_loc("Number of Vendors")] = "color: green"
    elif row.Category == 'Food':
        ret[row.index.get_loc("Number of Vendors")] = "color: orange"
    elif row.Category == 'Books':
        ret[row.index.get_loc("Number of Vendors")] = "color: blue"
    return ret
