from argparse import _MutuallyExclusiveGroup
from ast import Pass
from typing import Text
from django.db.models import indexes
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect ,HttpResponse
from django.contrib.auth import authenticate, login
from customuser.models import user_type, User
from django.shortcuts import render,HttpResponse ,redirect
from django.views import generic
from django.contrib import messages 
from geopy.geocoders import Nominatim
from datetime import datetime
from playsound import playsound
import math, random
import time
# from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate,  login, logout
import requests
from .models import Orders, PersonalDetails, Shop,Image,Prescription,GetDeliveries,Cities
from .models import StoreBill,ParselImage,NotificationReminder,UserManager,DeliveryPartner,Profile,SavedAddress
# from geopy.geocoders import Nominatim
from math import e, remainder, sin, cos, radians, degrees, acos
import math
from django.http import HttpResponseBadRequest
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import uuid
import itertools
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from newproject.settings import RAZORPAY_API_KEY
from newproject.settings import RAZORPAY_API_SECRET_KEY
import razorpay
from django.contrib.sites.shortcuts import get_current_site
import razorpay
import os
from twilio.rest import Client
from pytonik_time_ago.timeago import timeago
# import datetime

def home(request): 
    # product = []
    # list_ = Product.objects.all()
    # for i in list_:
    #     i.product_name = i.product_name[:25]
    #     product.append(i)
    # new_list = []
    # new_list = []
    # city_names = []
    # placeholder_city = ""
    # if request.user.is_authenticated and user_type.objects.get(user=request.user).is_user==True:
    #     new_list = Shop.objects.all()
    #     new_list = list()
    #     city_names = list()
    #     if request.user.is_authenticated:
    #         uname = request.user
    #         current_user = PersonalDetails.objects.filter(username= uname)
    #         city= str(current_user[0].city)
    #         address=str(current_user[0].address)   
    #         city_input = city
    #         ob = Cities.objects.all()
    #         current_city_dict = {}
    #         current_city = list()
    #         for j in ob:
    #             if j.city_name.lower() == city_input.lower():
    #                 current_city_dict = {
    #                 'city_name':j.city_name,
    #                 'state':j.state,
    #                 }
    #                 current_city.append(current_city_dict)  
    #         geolocator = Nominatim(user_agent="my_user_agent")
    #         country = 'india'
    #         state = current_city[0]['state']
    #         loc = geolocator.geocode(city+','+ country + ',' + state)
    #         lat1 = loc.latitude
    #         lon1 = loc.longitude
    #         ob = Shop.objects.all()
    #         my_list = {}
    #         new_list = list()
    #         for i in ob:
    #             lon2 = i.lon
    #             lat2 = i.lat 
    #             theta = lon1-lon2
    #             dist = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(theta))
    #             dist = math.acos(dist)
    #             dist = math.degrees(dist)
    #             miles = dist * 60 * 1.1515
    #             distance = miles * 1.609344
    #             distance = round(distance, 1)
    #             my_list= {
    #             'name':i.name,
    #             'city':i.city,
    #             'distance':distance,
    #             'address':i.address,
    #             'id':i.pk,
    #             }
    #             new_list.append(my_list)
    #         new_list.sort(key=lambda x: x["distance"])
    #         placeholder_city = address
    #     else:
    #         placeholder_city = 'Search for location'
    # # return render(request,'shops/home.html'
    # context = {'new_list':new_list,'product':product,'city_names':city_names,'placeholder_city':placeholder_city} 
    context = {}
    if request.user.is_authenticated:
        if user_type.objects.get(user=request.user).is_delivery == True:
            return render(request,'deliver/home/index.html',context) 
        elif user_type.objects.get(user=request.user).is_store == True:
            return render(request,'store/home/index.html',context)
        else:
            return render(request,'user/home/index.html',context)
    else:
        return render(request,'user/home/index.html',context)

def send_otp(mobile, otp):
    account_sid = "AC8c55da658680546cd2f069c440eb8629"
    auth_token = "ec07b7a628608ff0ce668cdafcb54024"
    client = Client(account_sid, auth_token)
    body = f"Thanks for connecting with us. Your Login OTP is: {otp}"
    # message = client.messages \
    #                 .create(
    #                      body=f"Thanks for connecting with us. Your Login OTP is: {otp}",
    #                      from_='+16513749253',
    #                      to=f'+91{mobile}')
    return None

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        username=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        mobile=request.POST['mobile']
        check_user = User.objects.filter(email = email).first()
        check_profile = Profile.objects.filter(mobile = mobile).first()
        
        if check_user or check_profile:
            context = {'message' : 'User already exists' , 'class' : 'danger' }
            return render(request,'accounts/register.html' , context)

        user = User.objects.create_user(email = email)
        user.first_name= fname
        user.last_name= lname
        user.mobile = mobile
        user.save()
        new_user = PersonalDetails(fname=fname,lname=lname,username=email,email=email,mob=mobile,lat=0,lon=0)
        new_user.save()
        current_user=User.objects.get(email=username)
        user_type(user=current_user,is_user = True).save()
        otp = str(random.randint(1000 , 9999))
        profile = Profile(user = email , mobile=mobile , otp = otp) 
        profile.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('otp')
    return render(request,'accounts/register.html')

def otp(request):
    context = {}
    if request.method == 'POST':
        mobile = request.session['mobile']
        context = {'mobile':mobile}
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        if otp == profile.otp:
            user = User.objects.get(email = profile.user)
            login(request , user)
            myuser = User.objects.get(email = profile.user)
            if user_type.objects.get(user=myuser).is_store==True:
                return redirect('/store-notifications')
            else:
                return redirect('/')   
        else:
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile }
            return render(request,'accounts/reg_otp.html' , context)

    return render(request,'accounts/reg_otp.html' , context)

url_list1 = []
def login_attempt(request):
    if request.GET.get('next') != None:
        next_url = request.GET.get('next')
    else:
        next_url = '/'
    url_list1.append(next_url)
    if len(url_list1) > 10:
        url_list1.pop(0)
    
    if request.method == 'POST':
        mobile = request.POST.get('mobile')  
        user = Profile.objects.filter(mobile = mobile).first()
        if user is None:
            context = {'message' : 'User not found' , 'class' : 'danger' }
            return render(request,'accounts/login.html' , context)
        otp = str(random.randint(1000 , 9999))
        user.otp = otp
        user.save()
        send_otp(mobile , otp)
        request.session['mobile'] = mobile
        return redirect('login_otp')      
    return render(request,'accounts/login.html')

def login_otp(request):
    last_url = url_list1[-1]
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        if otp == profile.otp:
            user = User.objects.get(email = profile.user)
            login(request , user)
            # if user_type.objects.get(user=user).is_delivery==True:
            #     return redirect('/get-delivery')
            # if user_type.objects.get(user=user).is_store==True:
            #     return redirect('/store-notifications')
            # else:
            return redirect(last_url)
        else:
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':mobile}
            return render(request,'accounts//login_otp.html' , context)
    return render(request,'accounts/login_otp.html' , context)

# Common-Data Sharing
def common(request):
    notification_url = '/'
    fname = ' '
    lname = ' '
    app_user_type = None
    noti_len = 0
    prof_fname = None
    prof_lname =None
    
    usermail = ''
    name= 'Welcome'
    my_url = request.path
    home_step = ''
    myorder_step = ''
    if my_url == '/':
        home_step = 'active'

    if my_url == '/myorders':
        myorder_step = 'active'
        bag_bg_clr = '#89dee2;'
    else:
        bag_bg_clr = 'black;'
    
    if request.user.is_authenticated and user_type.objects.exists():
        username = request.user
        prof_fname = PersonalDetails.objects.filter(username=str(username))[0].fname
        prof_lname = PersonalDetails.objects.filter(username=str(username))[0].lname
    
    if request.user.is_authenticated:
        if user_type.objects.get(user=request.user).is_delivery==True:
            noti_len = Orders.objects.filter(deliver_status = False).count()
            app_user_type = 'deliver'
            user = request.user
            myname = PersonalDetails.objects.filter(username = user)
            fname = myname[0].fname
            lname = myname[0].lname
            usermail = str(request.user)
            name = str(fname) + str(' ') + str(lname)

    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_user==True:
        notification_url = 'users-notifications'
        noti_len = Orders.objects.filter(order_completed = False).filter(c_username=str(request.user)).count()
        app_user_type = 'customer'
        user = request.user
        myname = PersonalDetails.objects.filter(username = user)
        fname = myname[0].fname
        lname = myname[0].lname
        usermail = str(request.user)
        name = str(fname) + str(' ') + str(lname)
        if request.POST.get('input_city_name'):
            current_city = request.POST.get('input_city_name')
        else:
            uname = request.user
            current_user = PersonalDetails.objects.filter(username= uname)
            current_city = str(current_user[0].city)
    else:
        if request.POST.get('input_city_name'):
            current_city = request.POST.get('input_city_name')
        else:
            current_city = "Search Location"

    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_store==True:
        notification_url = 'store-notifications'
        noti_len = Orders.objects.filter(order_accept_status = 'not_responded').count()
        usermail = str(request.user)
        app_user_type = 'store_owner'

    return {
        'current_city':current_city,'fname':fname,'app_user_type':app_user_type,'noti_len':noti_len,'prof_lname':prof_lname,
        'prof_fname':prof_fname,'name':name,'usermail':usermail,'home_step':home_step,'myorder_step':myorder_step,
        'bag_bg_clr':bag_bg_clr,'notification_url':notification_url,'lname':lname,} 

my_len = []
my_len2  = []
my_len3 = []
my_len4 = []
my_len5 = []
my_len6 = []
def CheckNOfitication(request):
    notification = None
    noti_url = None
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_store==True:
        allObj = Orders.objects.filter(s_username=request.user)
        try: 
            if len(my_len) ==5:
                my_len.pop(0)
        except:
            pass  
        try:
            if my_len[-1] < allObj.count():
                playsound('tones/Waterdrop_Drop.mp3',False)
                notification = {'notification':"You've got a new request."}
                noti_url = {'noti_url':'store-notifications'}
        except:
            pass
        my_len.append(allObj.count())
    
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_delivery==True:
        AllObjs = Orders.objects.filter(order_accept_status = 'accepted')
        PaymentComplited = [] 
        for i in AllObjs:
            if i.payment_status != 'not_responded':
                PaymentComplited.append(i)
        
        try: 
            if len(my_len2) ==5:
                my_len2.pop(0)
        except:
            pass  
        try:
            if my_len2[-1] < len(PaymentComplited):

                playsound('tones/Waterdrop_Drop.mp3',False)

                notification = {'notification':"You've got a new Delivery request."}
                noti_url = {'noti_url':'get-delivery'}
        except:
            pass
        my_len2.append(len(PaymentComplited))
    
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_user==True:
    #    First Notification
        AllObjs = Orders.objects.filter(is_bill_uploaded = True).filter(c_username=str(request.user))
        try:
            if len(my_len3) ==5:
                my_len3.pop(0)
        except:
            pass  
        try:
            if my_len3[-1] < AllObjs.count():
                playsound('tones/Waterdrop_Drop.mp3',False)
                notification = {'notification':"Your Medicine is ready please complete payment process"}
                
                noti_url = {'noti_url':'users-notifications'}
        except:
            pass
        my_len3.append(AllObjs.count())

        # Order Rejected --
        RejectedObjs = Orders.objects.filter(order_accept_status = 'rejected').filter(c_username=str(request.user))
        try:
            if len(my_len5) ==5:
                my_len5.pop(0)
        except:
            pass  
        try:
            if my_len5[-1] < RejectedObjs.count():
                playsound('tones/Waterdrop_Drop.mp3',False)
                notification = {'notification':"We are not able to accept your Order .."}
                noti_url = {'noti_url':'users-notifications'}
        except:
            pass
        my_len5.append(RejectedObjs.count())

    #Third Notification
        ThirdObjs = AllObjs.filter(is_parsel_uploaded = True)
        try:
            if len(my_len6) ==5:
                my_len6.pop(0)
        except:
            pass  
        try:
            if my_len6[-1] < ThirdObjs.count():
                playsound('tones/Waterdrop_Drop.mp3',False)
                notification = {'notification':"Your order is picked see parsel photo.."}
                noti_url = {'noti_url':'users-notifications'}
        except:
            pass
        my_len6.append(ThirdObjs.count())
    
    notification = notification

    # playsound('tones/Waterdrop_Drop.mp3',False)
    return JsonResponse({"notification":notification,'noti_url':noti_url},safe = False)

def search_results(request):
    if request.is_ajax():
        game = request.POST.get('game')
        qs = Cities.objects.filter(city_name__icontains = game) 
        if len(qs) > 0 and len(game) > 0:
            data = []
            item = {'name':"",}
            res = []
            for pos in qs:
                item = {
                'pk':pos.pk,
                'name':pos.city_name.capitalize(),
                'state':pos.state,
                }
                data.append(item)
                res = data[:10]
        else:
            res = ''
        return JsonResponse({'data':res})
    return render(request,'shops/home.html',{'data':res,'new_list':new_list})
 
def SearchProducts(request):
    if request.is_ajax():
        new_data = request.POST.get('new_data')
        qs = Product.objects.filter(product_name__icontains = new_data) 
        if len(qs) > 0 and len(new_data) > 0:
            data = []
            item = {'name':"",}
            res = []
            for pos in qs:
                item = {
                'pk':pos.pk,
                'name':pos.product_name.capitalize(),
                }
                data.append(item)
                res = data[:10]
        else:
            res = ''
        return JsonResponse({'data':res})
    return render(request,'shops/home.html')
    
@login_required(redirect_field_name='next',login_url = '/login')
def UploadPrescriptions(request):
    if request.user.is_authenticated:
        return redirect('/list-stores')
    else:
        return HttpResponse("Please login first")
    # return render(request,'shops/upload_prescription.html')                                   

@login_required(redirect_field_name='next',login_url = '/login')                
def upload(request,myid):
    product = ''
    previus_10 = []
    history = Image.objects.filter(user = request.user)[:10]
    for j in history:
        j.date = j.date.strftime("%b-%d-%Y") 
        previus_10.append(j)
    current_data=Shop.objects.filter(id = myid)
    id_ = myid
    name = current_data[0].name
    store_user = current_data[0].store_user
    city_name = current_data[0].city
    address = current_data[0].address 
    
    if request.POST.get('PresItems'):
        list_id = list()
        images_list = list()
        item_list = list()
        PresItems = json.loads(request.POST.get('PresItems', False))
        for i in PresItems:
            list_id.append(int(i))
        imgs_data = Image.objects.all()
        for img in imgs_data:
            if img.id in list_id:
                item_list.append(img)
                images_list.append(str(img.image))
        user=item_list[0].user
        store_user = item_list[0].store_user
        current_data=Shop.objects.filter(store_user = store_user)
        name = current_data[0].name
        store_user = current_data[0].store_user
        city_name = current_data[0].city
        address = current_data[0].address 
        list_img = list()
        item = images_list 
        if len(item) == 5:          
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=item[0],image2=item[1],image3=item[2],
            image4=item[3],image5=item[4],message='You have got request for medicines')
            new_data.save()
        elif len(item) == 4:
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=item[0],image2=item[1],image3=item[2],
            image4=item[3],message = 'You have got request for medicines')
            new_data.save()
        elif len(item) == 3:
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=item[0],image2=item[1],image3=item[2],message ='You have got request for medicines')
            new_data.save()
        elif len(item) == 2:
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=item[0],image2=item[1],message = 'You have got request for medicines')
            new_data.save()
        elif len(item) == 1:
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=item[0],message = 'You have got request for medicines')
            new_data.save()
        return redirect('/checkout')
    
    # Upload images from gallary--
    elif request.method == 'POST':
        data = request.FILES.getlist("images")
        desc = request.POST.get('instructions')
        for i in data:
            new_image = Image(image = i,user = request.user,store_user = store_user)
            new_image.save()
        if len(data) == 5:          
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=data[0],image2=data[1],image3=data[2],
            image4=data[3],image5=data[4],desc = desc,message='You have got request for medicines')
            new_data.save()
        elif len(data) == 4:
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=data[0],image2=data[1],image3=data[2],
            image4=data[3],desc = desc,message = 'You have got request for medicines')
            new_data.save()
        elif len(data) == 3:
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=data[0],image2=data[1],image3=data[2],desc = desc,message ='You have got request for medicines')
            new_data.save()
        elif len(data) == 2:
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=data[0],image2=data[1],desc = desc,message = 'You have got request for medicines')
            new_data.save()
        elif len(data) == 1:
            new_data = Prescription(sender= request.user,reciver = store_user,
            image1=data[0],desc = desc,message = 'You have got request for medicines')
            new_data.save()
        myurl = request.path
        obj = myurl.split('/')
        try:
            obj.index('app-view') 
            return redirect('/app-view/checkout')
        except:          
            return redirect('/checkout')
    context = {'id_':id_,'product':product,'previus_10':previus_10,'CurrentId':myid}
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        templates = 'app-view/user/home/upload-prescription.html'
    except:          
        templates = 'user/home/upload-prescription.html'
    return render(request,templates,context)

def image_upload(request):
    
    return render(request, 'index.html', context=context)

def SomeFunction(request):
    if request.is_ajax():
        list_id = list()
        item_list = list()
        cart_items = json.loads(request.GET.get('cart_items', False))
        for i in cart_items:
            list_id.append(int(i))
        imgs_data = Image.objects.all()
        for img in imgs_data:
            if img.id in list_id:
                item_list.append(img)
        user=item_list[0].user
        store_user = item_list[1].store_user
    
        My_Id = request.GET.get('MyId')
        current_data=Shop.objects.filter(id = My_Id)
        name = current_data[0].name
        store_user = current_data[0].store_user
        city_name = current_data[0].city
        address = current_data[0].address 
        
        # messages.success(request, "Your Prescriptions has been uploaded successfully..Please wait for 2 minutes..")
        new_notification = Notification(sender=user,reciver=store_user,
            message ='You have got request for medicines',viewed = False)
        new_notification.save()

    return render(request, 'shops/notificationview.html',{'data':item_list})
        
def list_stores(request):
    product = []
    if request.POST.get('input_city_name'):
        city_input = request.POST.get('input_city_name')
        ob = Cities.objects.all()
        current_city_dict = {}
        current_city = list()
        for j in ob:
            if j.city_name.lower() == city_input.lower():
                current_city_dict = {
                'city_name':j.city_name,
                'state':j.state,
                }
                current_city.append(current_city_dict)  
        geolocator = Nominatim(user_agent="my_user_agent")
        country = 'india'
        city = city_input
        state = current_city[0]['state']
        placeholder_city = f'{city}, {state}'
        loc = geolocator.geocode(city+','+ country + ',' + state)
        lat1 = loc.latitude
        lon1 = loc.longitude
        ob = Shop.objects.all()
        my_list = {}
        new_list = list()
        for i in ob:
            lon2 = float(i.lon)
            lat2 = float(i.lat)
            theta = lon1-lon2
            dist = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(theta))
            dist = math.acos(dist)
            dist = math.degrees(dist)
            miles = dist * 60 * 1.1515
            distance = miles * 1.609344
            distance = round(distance, 1)
            my_list= {
            'name':i.name,
            'city':i.city,
            'distance':distance,
            'address':i.address,
            'id':i.pk,
            }
            new_list.append(my_list)
        new_list.sort(key=lambda x: x["distance"])
        response_value = request.POST.get('input_response')
    else:
        new_list = Shop.objects.all()
        new_list = list()
        city_names = list()
        if request.user.is_authenticated:
            uname = request.user
            current_user = PersonalDetails.objects.filter(username= uname)
            city= str(current_user[0].city)
            address=str(current_user[0].address)
            city_input = city
            ob = Cities.objects.all()
            current_city_dict = {}
            current_city = list()
            for j in ob:
                if j.city_name.lower() == city_input.lower():
                    current_city_dict = {
                    'city_name':j.city_name,
                    'state':j.state,
                    }
                    current_city.append(current_city_dict)  
            geolocator = Nominatim(user_agent="my_user_agent")
            country = 'india'
            state = current_city[0]['state']
            loc = geolocator.geocode(city+','+ country + ',' + state)
            lat1 = loc.latitude
            lon1 = loc.longitude
            ob = Shop.objects.all()
            my_list = {}
            new_list = list()
            for i in ob:
                lon2 = float(i.lon)
                lat2 = float(i.lat)
                theta = lon1-lon2
                dist = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(theta))
                dist = math.acos(dist)
                dist = math.degrees(dist)
                miles = dist * 60 * 1.1515
                distance = miles * 1.609344
                distance = round(distance, 1)
                my_list= {
                'name':i.name,
                'city':i.city,
                'distance':distance,
                'address':i.address,
                'id':i.pk,
                }
                new_list.append(my_list)
            new_list.sort(key=lambda x: x["distance"])
            placeholder_city = address
        else:
            placeholder_city = 'Search for location'
    return render(request,'shops/home.html',{'new_list':new_list,
        'hide_prescription':True,'product':product,'placeholder_city':placeholder_city})

def StoreList(request):
    
    return render(request,'shops/store_list.html')

@login_required(redirect_field_name='next',login_url = '/login')
def medical_store_view(request,myid,st_name,st_dist):
    data = Shop.objects.filter(id = myid)
    distance = st_dist[1:]
    name = data[0].name
    store_user = data[0].store_user
    city_name = data[0].city
    address = data[0].address 
    id_ = myid
    if request.method == 'POST':
        display_type = request.POST.get('is_conditions' or None)    
        myfile = request.FILES["image_file"] 
        user_id = request.user
        saved = Image(image=myfile,user=request.user,store_user=store_user)
        saved.save()

    else:
        pass

    context =  {'name':name,'city_name':city_name,'address':address,'distance':distance,'myid':myid,'id_':id_}
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        templates = 'app-view/user/home/store-view.html'
    except:          
        templates = 'user/home/store-view.html'
    return render(request,templates,context)
   #Login Page

def UserLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/user-login")
    else:
        return render(request,'user/home/sign-in.html')

def handleSignUp(request):
    if request.method=="POST":
        username=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        mobile=request.POST['mobile']
        city=request.POST['city']
        address=request.POST['address']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if len(username)<6:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')
        # if not username.isalnum():
        #     messages.error(request, " User name should only contain letters and numbers")
        #     return redirect('home')
        if (pass1!= pass2):
            messages.error(request, " Passwords do not match")
            return redirect('home')

        myuser = User.objects.create_user(username, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.mobile = mobile
        myuser.city = city
        myuser.address = address
        myuser.save()
        new_user = PersonalDetails(fname=fname,lname=lname,username=username,email=email,mob=mobile,city=city,address=address)
        new_user.save()
        current_user=User.objects.get(email=username)
        user_type(user=current_user,is_user = True).save()
        messages.success(request, " Your Account has been successfully created. Please Login")
        return redirect('home')
    else:
        return HttpResponse("404 - Not found")

def OTP(request):
    request.session['mobile'] = 9108085748
    my_num = request.session['mobile']
    return my_num

url_list = [] 
def handeLogin(request):
    next_url = request.GET.get('next')
    url_list.append(next_url)
    if len(url_list) > 10:
        url_list.pop(0)
    last_url = url_list[-1]
    if request.method=="POST":   
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            return redirect(last_url)
        else:
            messages.error(request, "Invalid credentials! Please try again")
            

    return render(request,'user/home/sign-in.html')
    return HttpResponse("login")

def handelLogout(request):
    logout(request)
    return redirect('/login')

def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/forget-password/')
            
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')
    
    except Exception as e:
        pass
    return render(request , 'shops/forget-password.html')

def ChangePassword(request , token):
    context = {}
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')

            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login/')        
    except Exception as e:
        pass
    return render(request , 'shops/change-password.html' , context)

def Send_Notification(request):
           
# def Send_Notification(request):
#     import os
#     from twilio.rest import Client
#     account_sid = "AC8c55da658680546cd2f069c440eb8629"
#     auth_token = "ec07b7a628608ff0ce668cdafcb54024"
#     client = Client(account_sid, auth_token)
#     message = client.messages \
#                     .create(
#                          body="Hello World",
#                          from_='+14433414796',
#                          to='+919108085748'
#                      ) 
    pass
   
@login_required(redirect_field_name='next',login_url = '/login')
def show_notifications(request,user_name):
    return render(request,'shops/notificationview.html')

def get_users_notifications(request):
    is_user = False
    is_store = False
    # Notifications for Stores
    new_data = None
    type_obj = user_type.objects.get(user=request.user)
    if request.user.is_authenticated and type_obj.is_store==True:
        is_store = True
        allObj = Orders.objects.filter(s_username=request.user)
        latestObj = allObj.order_by('-date')[:5]
        messages1 = []
        my_dict = {}
        items = []
        for i in latestObj:  
            sendername = str(PersonalDetails.objects.filter(username=i.c_username)[0].fname) + str(' ') + str(PersonalDetails.objects.filter(username=i.c_username)[0].lname)
            shopob = Shop.objects.filter(store_user=request.user)
            photo = shopob[0].storephoto 
            if i.order_accept_status == 'not_responded':
                which_color = '#C0C0C0;'
            else:
                which_color = '#F5F5F5;'
            # Time Ago 
            time = i.date.strftime('%H:%M:%S')
            date = i.date.date()
            mixed = str(date) + str(time)
            time_ago = timeago(f"{str(date)} {str(time)}").ago
            # create dictionary
            my_dict = {
                'senderId':i.c_username,
                'sender':sendername,
                'reciver':i.s_username,
                'id':i.id,
                'date':time_ago,
                'message':i.store_notification_1,
                 'photo':str(photo),
                'which_color':which_color,
            }
            messages1.append(my_dict)
            new_data = messages1

    noti_for_users = None
    type_obj = user_type.objects.get(user=request.user)
    # Notifications for users
    if request.user.is_authenticated and type_obj.is_user==True:
        is_user = True
        objs =  my_notif = Orders.objects.filter(c_username=request.user).order_by('-date')[:5]
        messages1 = []
        my_dict = {}
        items = []
        new_data = None
        for i in objs:  
            sendername = str(PersonalDetails.objects.filter(username=i.s_username)[0].fname) + str(' ') + str(PersonalDetails.objects.filter(username=i.s_username)[0].lname)
            if i.order_completed == False:
                which_color = '#C0C0C0;'
            else:
                which_color = '#F5F5F5;'

            shopob = Shop.objects.filter(store_user=i.s_username)
            photo = shopob[0].storephoto
             # Time Ago 
            time = i.date.strftime('%H:%M:%S')
            date = i.date.date()
            mixed = str(date) + str(time)
            time_ago = timeago(f"{str(date)} {str(time)}").ago

            my_dict = {
                'sender':sendername,
                'senderId':i.s_username,
                'reciver':i.c_username,
                'id':i.id,
                'date':time_ago,
                'message':f'You have recied notification for order id DH231K{i.id}',
                'which_color':which_color,
                'photo':str(photo),
            }
            messages1.append(my_dict)
            noti_for_users = messages1

    return JsonResponse({'messages1':new_data,"noti_for_users":noti_for_users,
    'is_store':is_store,'is_user':is_user},safe=False)
    
    return render(request,'shops/notificationview.html',{'col':'green'})

@login_required(redirect_field_name='next',login_url = '/login')
def notification_view(request):
    data = None
    latest_notification = None
    time = None
    user_name = request.user
    type_obj = user_type.objects.get(user=request.user)
    notification = None
    IsAccepted = None
    text = None
    if request.user.is_authenticated and type_obj.is_store==True:  
        user_noti_1 = 'Thanks for ordering.. Your delivery request has been accepted choose your payment method and go ahed'
        if request.POST.get('store_response'):
            store_response = request.POST.get('store_response')
            DataId = request.POST.get('data_id')
            is_accepted = store_response[:8]
            which_user = store_response[9:]
            if str(is_accepted) == 'accpeted':
                SelectedStore = Orders.objects.filter(id=DataId).update(user_notification_1 = user_noti_1,order_accept_status='accepted')
                new_delivery = GetDeliveries(storeuser= request.user,customername=which_user,respondstatus = 'not-responded',price = 0,
                orderid=DataId)
                new_delivery.save()
                # UPDATE user and store details
                shop_list = Shop.objects.all()
                customer_data = PersonalDetails.objects.all()
                requestlist = GetDeliveries.objects.all()
                
                for i in requestlist:
                    current_store_name = i.storeuser 
                    listed = shop_list.filter(store_user = current_store_name)
                    GetDeliveries.objects.filter(id = i.id).update(storeaddress = listed[0].address,storemobile=listed[0].mobile,storecity = listed[0].city)
                
                for j in customer_data:
                    customer_name = j.username
                    listed = customer_data.filter(username = customer_name) 
                    GetDeliveries.objects.filter(id = j.id).update(customeraddress = listed[0].address,customermobile=listed[0].mob)
                text = f"You have accpeted delivery request of {which_user}"
                # Update Prescrition Status -- Accpted
                Prescription.objects.filter(id = DataId).update(responed_status='accepted')
                # PlacedOrders.objects.filter(images = DataId).update(store_status = True)
                # IsAccepted = PlacedOrders.objects.filter(images = DataId)[0]
                # text = f"You have Rejected delivery request of {which_user}"
                myurl = request.path
                obj = myurl.split('/')
                try:
                    obj.index('app-view') 
                    return redirect(f"/app-view/store-order-response/{DataId}")
                except:        
                    return redirect(f"/store-order-response/{DataId}")
            else:
                user_noti_1 = 'We are not able to accept your request.  '
                Orders.objects.filter(id=DataId).update(user_notification_1 = user_noti_1,order_accept_status='rejected')
                return redirect(f"/store-order-response/{DataId}")

    if request.user.is_authenticated and type_obj.is_user==True:
        objs =  my_notif = Orders.objects.filter(c_username=request.user).order_by('-date')[:10]
        messages1 = []
        my_dict = {}
        items = []
        new_data = None
        for i in objs:  
            # if i.order_accept_status == 'not_responded':
            #     which_color = '#C0C0C0;'
            # else:
            #     which_color = '#F5F5F5;'
            my_dict = {
                'sender':i.s_username,
                'reciver':i.c_username,
                'id':i.id,
                'date':i.date.strftime('%H:%M:%S'),
                'message':i.store_notification_1,
                # 'which_color':which_color,
            }
            messages1.append(my_dict)
        # return JsonResponse({'messages1':messages1},safe=False)
    return render(request,'shops/notificationview.html',
    {'type_obj':type_obj,'IsAccepted':IsAccepted,
        'text':text,'notification':notification,'data':data,
        })

@login_required(redirect_field_name='next',login_url = '/login')
def StoreNotifications(request):
    type_obj = user_type.objects.get(user=request.user)
    if request.user.is_authenticated and type_obj.is_store==True:
        is_store = True
        allObj = Orders.objects.filter(s_username=request.user)
        latestObj = allObj.order_by('-date')[:5]
        messages1 = []
        my_dict = {}
        items = []
        for i in latestObj:  
            sendername = str(PersonalDetails.objects.filter(username=i.c_username)[0].fname) + str(' ') + str(PersonalDetails.objects.filter(username=i.c_username)[0].lname)
            shopob = Shop.objects.filter(store_user=request.user)
            photo = shopob[0].storephoto 
            if i.order_accept_status == 'not_responded':
                which_color = '#C0C0C0;'
            else:
                which_color = '#F5F5F5;'
            # Time Ago 
            time = i.date.strftime('%H:%M:%S')
            date = i.date.date()
            mixed = str(date) + str(time)
            time_ago = timeago(f"{str(date)} {str(time)}").ago
            # create dictionary
            my_dict = {
                'senderId':i.c_username,
                'sender':sendername,
                'reciver':i.s_username,
                'id':i.id,
                'date':time_ago,
                'message':i.store_notification_1,
                 'photo':str(photo),
                'which_color':which_color,
            }
            messages1.append(my_dict)
            
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        templates = 'app-view/store/home/request.html'
    except:          
        templates = 'store/home/request.html'

    context = {'messages_list':messages1} 
    return render(request,templates,context)

def UsersNotifications(request):
    # Notifications for users
    type_obj = user_type.objects.get(user=request.user)
    if request.user.is_authenticated and type_obj.is_user==True:
        is_user = True
        objs =  my_notif = Orders.objects.filter(c_username=request.user).order_by('-date')[:5]
        messages1 = []
        my_dict = {}
        items = []
        new_data = None
        for i in objs:  
            sendername = str(PersonalDetails.objects.filter(username=i.s_username)[0].fname) + str(' ') + str(PersonalDetails.objects.filter(username=i.s_username)[0].lname)
            if i.order_completed == False:
                which_color = '#C0C0C0;'
            else:
                which_color = '#F5F5F5;'

            shopob = Shop.objects.filter(store_user=i.s_username)
            photo = shopob[0].storephoto
             # Time Ago 
            time = i.date.strftime('%H:%M:%S')
            date = i.date.date()
            mixed = str(date) + str(time)
            time_ago = timeago(f"{str(date)} {str(time)}").ago

            my_dict = {
                'sender':sendername,
                'senderId':i.s_username,
                'reciver':i.c_username,
                'id':i.id,
                'date':time_ago,
                'message':f'You have recied notification for order id DH231K{i.id}',
                'which_color':which_color,
                'photo':str(photo),
            }
            messages1.append(my_dict)
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        templates = 'app-view/user/home/notifications.html'
    except:          
        templates = 'user/home/notifications.html'

    context = {'messages_list':messages1}
    return render(request,templates,context)

def notification_view_details(request,current_user,myid):
    type_obj = user_type.objects.get(user=request.user)
    notification = None
    new_data = []
    text = ""
    if request.user.is_authenticated and type_obj.is_store==True:
        order_details = Orders.objects.filter(id=myid)
        images_id = order_details[0].images_id
        for j in order_details:
            j.date = j.date.strftime('%H:%M:%S')
            new_data.append(j)
        inbox_items = order_details[0].inbox_items
        items_dict = {}
        items_list = []
        prod_len = 0
        if len(inbox_items) >= 1:
            inbox_items = json.loads(inbox_items)
            for i in inbox_items:
                for item in i:
                    prod_name=i[item][0] 
                    prod_pack = i[item][1]
                    qty = i[item][2]
                    items_dict = {
                        'Product':prod_name,
                        'Pack':prod_pack,
                        'Quantity':qty,
                    }
                    prod_len = prod_len + len(prod_name)
                    items_list.append(items_dict)
        if prod_len <= 1:
            Items_show = False
        else:
            Items_show = True
            
        cart_items = order_details[0].items 
        ResponStatus = order_details[0].order_accept_status
        Is_responsed = False
        if ResponStatus == 'accepted':
            Is_responsed = True
            text = 'You have accpeted delivery request'
        elif ResponStatus == 'rejected':
            Is_responsed = True
            text = 'You have rejected delivery request'  
        data = []
        reqeust_sender = order_details[0].c_username
        images_data = ''
        try:
            all_data = Image.objects.filter(store_user=request.user).filter(user=current_user).order_by('-date')
            last_item = Image.objects.filter(user=reqeust_sender).filter(store_user=request.user).last()
            last_time = last_item.date
            last_time = last_time.strftime('%H:%M:%S')
            for i in all_data:
                if i.date.strftime('%H:%M:%S')[:5] == last_time[:5]:
                    if len(i.desc) < 2:
                        i.desc = ""
                        data.append(i)
                    else:
                        data.append(i)
            pres_data = Prescription.objects.filter(id=images_id)
            IsIns = False
            instructions = pres_data[0].desc
            if len(instructions) > 5:
                IsIns = True    
            pers_dict = {}
            for pers in pres_data:
                if pers.image1 != 'default.jpg':
                    pers_dict[0] = pers.image1            
                if pers.image2 != 'default.jpg':
                    pers_dict[1] = pers.image2 
                if pers.image3 != 'default.jpg':           
                    pers_dict[2] = pers.image3 
                if pers.image4 != 'default.jpg':
                    pers_dict[3] = pers.image4 
                if pers.image5 != 'default.jpg':
                    pers_dict[4] = pers.image5
            images_data = []
            for img in range(len(pers_dict)):
                images_data.append(pers_dict[img])
            
        except:
            pass

        IsAccepted = order_details[0]
    context = {
        'data':data,'new_data':new_data,'type_obj':type_obj,'myid':myid,'text':text,'Is_responsed':Is_responsed,
        'ResponStatus':ResponStatus, 'items_list':items_list,'cart_items':cart_items,
        'IsAccepted':IsAccepted,'Items_show':Items_show, 'images_data':images_data,
        'IsIns':IsIns,'instructions':instructions}
    
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        url_path = 'app-view/store/home/notification-view.html'
    except:          
        url_path = 'store/home/notification-view.html'
    return render(request,url_path,context)

def UsersNotificationDetails(request,current_user,myid):
    UsersNotifications1 = Orders.objects.filter(id=myid)
    UsersNotifications = []
    rejection_reason = None
    for i in UsersNotifications1:
        # Time Ago 
        time = i.date.strftime('%H:%M:%S')
        date = i.date.date()
        mixed = str(date) + str(time)
        time_ago = timeago(f"{str(date)} {str(time)}").ago
        i.date = time_ago
        UsersNotifications.append(i)
    UsersNotifications =UsersNotifications[0]
    Parsel_Details = []
    new_list = []
    if UsersNotifications.is_parsel_uploaded == True:
        Parsel_Details = []
        new_list = ParselImage.objects.filter(order_id = myid)
        for parsel in new_list:
            # Time Ago 
            time = parsel.date.strftime('%H:%M:%S')
            date = parsel.date.date()
            mixed = str(date) + str(time)
            time_ago = timeago(f"{str(date)} {str(time)}").ago

            parsel.date = time_ago
            Parsel_Details.append(parsel)
        Parsel_Details = Parsel_Details[0]

    if UsersNotifications.order_accept_status == 'accepted':
        message_2 = 'Thanks for ordering.. Your delivery request has been accepted go to payment details ..'
    elif UsersNotifications.order_accept_status == 'rejected':
        message_2 = 'Your delivery request has been rejected..'
        rejection_reason = UsersNotifications.rejection_reason
    else:
        message_2 = ''
    if UsersNotifications.images_id != " ":
        message_1 = 'Your Prescription has been uploaded Successfully.'
    else:
        message_1 = 'Your Medicines has been uploaded Successfully.'
    IsUser = True
    bill_image_store = []
    if StoreBill.objects.filter(order_id=myid).exists():
        bill_image_store1 =StoreBill.objects.filter(order_id=myid)
        for j in bill_image_store1:
            j.date =  j.date.strftime('%H:%M:%S')
            bill_image_store.append(j)
        bill_image_store =bill_image_store[-1]
    params = {'UsersNotifications':UsersNotifications,
    'IsUser':IsUser,
    'bill_image_store':bill_image_store,
    'message_1':message_1,'message_2':message_2,'rejection_reason':rejection_reason,'myid':myid,
    'Parsel_Details':Parsel_Details,
    }    
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        url_path = 'app-view/user/home/notification-view.html'
    except:          
        url_path = 'user/home/notification-view.html'

    return render(request,url_path,params)

item_list = []
pres_list = []
@login_required(redirect_field_name='next',login_url = '/login')
def CheckOut(request):
    myurl = request.path
    data = None
    if request.is_ajax() and request.POST.get('data'):
        inputdata = request.POST.get('data')
        data = json.loads(inputdata)
        item_list.append(data)
        return JsonResponse({'data':data,'item_list':item_list})

    if request.is_ajax() and request.POST.get('newaddress'):
        if request.POST.get('newaddress'):
            inputdata = request.POST.get('newaddress')
            inputdata = json.loads(inputdata)
            SavedAddress(username = str(request.user),room_no = inputdata[0], landmark = inputdata[1]).save()
            new_add_data = {'floor':inputdata[0],'landmark':inputdata[1]}
        return JsonResponse({'inputdata':new_add_data})

    if request.is_ajax():
        saved_address = SavedAddress.objects.filter(username=str(request.user))
        item = {}
        saved_address_list= []
        for add in saved_address:
            item = {
            'floor_no':add.room_no,
            'landmark':add.landmark.capitalize()
            }
            saved_address_list.append(item)
        return JsonResponse({'addresslist':saved_address_list})
    
    IsPrescription = None
    username = request.user
    IsOldCustomer = None
    OldCheckout = None
    pres_data = None
    pred_id = ''
    images_data = None

    # Without Prescription
    
    if request.POST.get('selected_store'):
        storeid = request.POST.get('selected_store')
        current_data=Shop.objects.filter(id = int(storeid))
        store_user = current_data[0].store_user
        reciver = store_user
        pres_list.append(reciver)

    try: 
        reciver = pres_list[-1]
        if len(pres_list) > 5:
            pres_list.pop(0)
    except:
        reciver = pres_list
   
    try:
        last_id = Prescription.objects.filter(sender = request.user).last().id
        pres_data = Prescription.objects.filter(id=last_id)
        pers_dict = {}  
        for pers in pres_data:
            if pers.image1 != 'default.jpg':
                pers_dict[0] = pers.image1            
            if pers.image2 != 'default.jpg':
                pers_dict[1] = pers.image2 
            if pers.image3 != 'default.jpg':           
                pers_dict[2] = pers.image3 
            if pers.image4 != 'default.jpg':
                pers_dict[3] = pers.image4 
            if pers.image5 != 'default.jpg':
                pers_dict[4] = pers.image5
        images_data = []
        for img in range(len(pers_dict)):
            images_data.append(pers_dict[img])
        pred_id = pres_data[0].id
        reciver = Prescription.objects.filter(id= pred_id)[0].reciver
    except:
        pass


    FullName = ''
    if Orders.objects.filter(c_username = request.user).exists():
        PersName = PersonalDetails.objects.filter(username = request.user)[0]
        FullName = str(PersName.fname) + str(' ') + str(PersName.lname) 
        PersonalDetails.objects.filter(username = request.user)[0].fname 
        IsOldCustomer = True
        OldCheckout = Orders.objects.filter(c_username = request.user).last()
    else:
        IsOldCustomer = False

    if request.POST.get('selected_address'):
        selected_address = request.POST.get('selected_address')
        selected_products = request.POST.get('selected_products')   
        ob = SavedAddress.objects.filter(username=str(request.user))[int(selected_address)]
        Address = str(ob.landmark) + str(',') + str(ob.room_no)
        customername = request.POST.get('inputname')
        address = Address
        city = ''
        flat_no = ob.room_no
        pincode = '416101'
        items = ''
        new_inbox_items = selected_products
        # Creating new_inbox_items 
        store_noti_1 = 'You have got request for medicines'
        if customername == '':   
            if Orders.objects.filter(c_username=username).exists():
                PrevOrder = Orders.objects.filter(c_username=str(request.user)).last()
                new_order = Orders(c_username = username,s_username = reciver,images_id = pred_id,
                            items=items,inbox_items=new_inbox_items,city=PrevOrder.city,
                            address =PrevOrder.address,
                            phone=PrevOrder.phone,pincode=PrevOrder.pincode,
                            store_notification_1 = store_noti_1)
                new_order.save()
        else:
            new_order = Orders(c_username = username,s_username = reciver,images_id = pred_id,
                                items=items,inbox_items=new_inbox_items,city=city,flat_no = flat_no,
                                address =address,pincode=pincode,store_notification_1 = store_noti_1)
            new_order.save()
        last_order = Orders.objects.filter(c_username=str(request.user)).last().id
        new_id = Orders.objects.filter(images_id = pred_id)[0].id
        Orders.objects.filter(images_id = pred_id).update(orderid = new_id)
        NotificationReminder(order_id = last_order).save()
        myurl = request.path
        obj = myurl.split('/')
        try:
            obj.index('app-view') 
            return redirect('/app-view/home')
        except:        
            return redirect('/')

    context = {'OldCheckout':OldCheckout,'IsOldCustomer':IsOldCustomer,'pres_data':pres_data,'images_data':images_data,
        IsPrescription:'IsPrescription','pred_id':pred_id,'FullName':FullName,
        'data':data}
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        templates = 'app-view/user/home/checkout.html'
    except:          
        templates = 'user/home/checkout.html'
    return render(request,templates,context)
# Profile --- 
@login_required(redirect_field_name='next',login_url = '/login')
def MyProfile(request,fname,lname):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        address = request.POST.get('address')
        city = request.POST.get('city')
        mobile = request.POST.get('mobile')
        PersonalDetails.objects.filter(username = str(request.user)).update(fname = fname,lname =lname,
        mob= mobile,city = city,address = address)
        return redirect(f'/users/{fname}-{lname}/profile')
        
    user = request.user
    myname = PersonalDetails.objects.filter(username = user)
    address = myname[0].address
    city = myname[0].city
    fname = myname[0].fname
    lname = myname[0].lname
    usermail = str(request.user)
    name = str(fname) + str(' ') + str(lname)
    mobile = myname[0].mob

    context = {'name':name,'usermail':usermail,'city':city,'fname':fname,'lname':lname,'address':address,
    'mobile':mobile,
    }
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        templates = 'app-view/user/home/profile.html'
    except:          
        templates = 'user/home/profile.html'
    return render(request,templates,context)
    
def AppMyProfile(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        address = request.POST.get('address')
        city = request.POST.get('city')
        mobile = request.POST.get('mobile')
        PersonalDetails.objects.filter(username = str(request.user)).update(fname = fname,lname =lname,
        mob= mobile,city = city,address = address)
        return redirect(f'/users/{fname}-{lname}/profile')
        
    user = request.user
    myname = PersonalDetails.objects.filter(username = user)
    address = myname[0].address
    city = myname[0].city
    fname = myname[0].fname
    lname = myname[0].lname
    usermail = str(request.user)
    name = str(fname) + str(' ') + str(lname)
    mobile = myname[0].mob

    context = {'name':name,'usermail':usermail,'city':city,'fname':fname,'lname':lname,'address':address,
    'mobile':mobile,
    }
    templates = 'app-view/user/home/profile.html'
    return render(request,templates,context)
    


def NewMyProfile(request):
    context = 'items'
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        templates = 'app-view/user/home/my-addresses.html'
    except:          
        templates = 'user/home/my-addresses.html'
    return render(request,templates,context)

@login_required(redirect_field_name='next',login_url = '/login')
def MyAddresses(request):
    sel_add_list = []
    if request.POST.get('confirmed_delete'):
        myid = request.POST.get('confirmed_delete')
        print(myid)
        SavedAddress.objects.filter(id=myid).delete()

    if request.POST.get('addressvalue'):
        sel_id = request.POST.get('addressvalue')
        floorno = request.POST.get('floorno')
        landmark = request.POST.get('landmark')
        SavedAddress.objects.filter(id=sel_id).update(landmark = landmark, room_no = floorno)
    if request.is_ajax():
        sel_id = request.POST.get('data')
        selected_address = SavedAddress.objects.filter(id=sel_id)
        sel_add_dict = {'lm': selected_address[0].landmark,
        'rn': selected_address[0].room_no,
        }
        sel_add_list.append(sel_add_dict)
        return JsonResponse({'selected_address':sel_add_list})
    try:
        addresses = SavedAddress.objects.filter(username = str(request.user))
    except:
        pass
        addresses = ''
    context = {'items':'item','addresses':addresses}
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        templates = 'app-view/user/home/my-addresses.html'
    except:          
        templates = 'user/home/my-addresses.html'
    return render(request,templates,context)

@login_required(redirect_field_name='next',login_url = '/login')
def MyOrders(request):
    myorders = []
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_user==True:
        if request.method == 'POST':
            input_id = request.POST.get('inputid')
            ord = Orders.objects.filter(id =input_id)
            time = ord[0].date.strftime('%H:%M:%S')
            date = ord[0].date.date()
            mixed = str(date) + str(time)
            time_ago = timeago(f"{str(date)} {str(time)}").ago
            try:
                if time_ago.split(' ')[1] == 'minutes':
                    if int(time_ago.split(' ')[0]) > 5:
                        pass
                    else: 
                        ord.update(is_cancelled = True)
                        # Calling Send Notification function to store ...
                        
            except:
                pass
        data = Orders.objects.filter(c_username = str(request.user)).order_by('-date')[:5]
        for i in data:
            ShopOb = Shop.objects.get(store_user = i.s_username)
            i.date = i.date.strftime("%b-%d-%Y") 
            newdict = {
                's_name':ShopOb.name,
                's_photo':ShopOb.storephoto,
                'date':i.date,
                'id':i.id,
                'order_completed':i.order_completed,
                'is_cancelled':i.is_cancelled,
            }
            myorders.append(newdict)

    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        url_path = 'app-view/user/home/myorder.html'
    except:          
        url_path = 'user/home/myorder.html'
    return render(request,url_path,{ 'myorders':myorders})

@login_required(redirect_field_name='next',login_url = '/login')
def MyAddress(request,fname,lname):
    return render(request,'shops/myaddress.html')

def GoogleMap(request):
    return render(request,'shops/googlemap.html')

def ProductView(request,myid):
    product = Product.objects.filter(id = myid)
    product = product[0]
    Item = Product.objects.all()
    desc = product.desc
    benefits = product.benefits
    use_directions = product.use_directions
    safety_info = product.safety_info
    ingradients = product.ingradients

    desc = desc.split('.')
    benefits = benefits.split('.')
    use_directions = use_directions.split('.')
    safety_info = safety_info.split('.')
    ingradients = ingradients.split('.')
    
    return render(request,'shops/product_view.html',{
        "product":product,'desc':desc,'benefits':benefits,'use_directions':use_directions,
        'safety_info':safety_info,'ingradients':ingradients,'Item':Item,
        })

#  def GetDelivery(request):
#     shop_list = Shop.objects.all()
#     request_list = Orders.objects.all()
#     current_deliver = PersonalDetails.objects.filter(username=request.user)
#     if request.POST:
#         deliver = PersonalDetails.objects.filter(username = request.user)[0]
#         delivername = str(deliver.fname) + str(deliver.lname)
#         delivermobile = deliver.mob
#         response_id = request.POST.get('accept_btn')
#         TrackOrderChange(request,response_id)
#         Orders.objects.filter(id=response_id).update(d_response_status = True,d_username=str(request.user),deliver_status=True)
#         return redirect('/get-delivery')
        
#     store_lat = float(current_deliver[0].lat)
#     store_lon = float(current_deliver[0].lon)
#     for k in request_list:
#         if k.order_accept_status == 'accepted':
#             StoreUser = k.s_username
#             ShopName = shop_list.filter(store_user = StoreUser)[0].name
#             ShopLat = shop_list.filter(store_user = StoreUser)[0].lat  
#             ShopLon = shop_list.filter(store_user = StoreUser)[0].lon
#         # calculate distance between from shop to delivery boy
#             my_list = {}
#             new_list = list()
#             lon2 = float(ShopLon)
#             lat2 = float(ShopLat)
#             theta = store_lon-lon2
#             dist = math.sin(math.radians(store_lat)) * math.sin(math.radians(lat2)) + math.cos(math.radians(store_lat)) * math.cos(math.radians(lat2)) * math.cos(math.radians(theta))
#             dist = math.acos(dist)
#             dist = math.degrees(dist)
#             miles = dist * 60 * 1.1515
#             distance = miles * 1.609344
#             distance = round(distance, 1)
#             Orders.objects.filter(s_username = StoreUser).filter(id=k.id).update(dist_d_to_s = distance)
#             AllDeliveries = Orders.objects.all().order_by('-date')
#             Deliver_dict = {}
#             Deliver_list = []
#             for i in AllDeliveries:
#                 if i.order_accept_status == 'accepted':
#                     if Shop.objects.filter(store_user=i.s_username).exists():
#                         shopdata=Shop.objects.filter(store_user=i.s_username)[0]
#                         storename = shopdata.name
#                         store_address = shopdata.address
#                         storecity = shopdata.city
#                         storedistance = distance
#                         date = i.date.strftime('%H:%M:%S')
#                         Deliver_dict= {
#                             'store_name':storename,
#                             'store_address':store_address,
#                             'storecity':storecity,
#                             'storedistance':storedistance,
#                             'id':i.id,
#                             'date':date,
#                             'respondstatus':i.d_response_status,
#                         }
#                         Deliver_list.append(Deliver_dict)
#     return render(request,'shops/delivery_page.html',{'Deliver_list':Deliver_list})

@login_required(redirect_field_name='next',login_url = '/login')
def DeliveryRequests(request,myid):
    shop_list = Shop.objects.all()
    request_list = Orders.objects.filter( id = myid)
    request_list = request_list[0]
    current_deliver = PersonalDetails.objects.filter(username=request.user)
    store_lat = float(current_deliver[0].lat)
    store_lon = float(current_deliver[0].lon)
    shopdata=Shop.objects.filter(store_user=request_list.s_username)[0]
    storename = shopdata.name
    store_address = shopdata.address
    storecity = shopdata.city
    storedistance = 1.2
    date = request_list.order_accept_time
    Deliver_dict = {}
    Deliver_list = []
    Deliver_dict= {
        'store_name':storename,
        'store_address':store_address,
        'storecity':storecity,
        'storedistance':storedistance,
        'id':request_list.id,
        'date':date,
        'respondstatus':request_list.deliver_status,
        'is_timeup':request_list.is_timeup,
    }
    Deliver_list.append(Deliver_dict)
    return Deliver_list
    # if request.user.is_authenticated and user_type.objects.get(user=request.user).is_delivery==True: 
        # shop_list = Shop.objects.all()
        # request_list = Orders.objects.all()
        # current_deliver = PersonalDetails.objects.filter(username=request.user)
        # store_lat = float(current_deliver[0].lat)
        # store_lon = float(current_deliver[0].lon)
        # for k in request_list:
        #     if k.order_accept_status == 'accepted':
        #         StoreUser = k.s_username
        #         ShopName = shop_list.filter(store_user = StoreUser)[0].name
        #         ShopLat = shop_list.filter(store_user = StoreUser)[0].lat  
        #         ShopLon = shop_list.filter(store_user = StoreUser)[0].lon
        #     # calculate distance between from shop to delivery boy
        #         my_list = {}
        #         new_list = list()
        #         lon2 = float(ShopLon)
        #         lat2 = float(ShopLat)
        #         theta = store_lon-lon2
        #         dist = math.sin(math.radians(store_lat)) * math.sin(math.radians(lat2)) + math.cos(math.radians(store_lat)) * math.cos(math.radians(lat2)) * math.cos(math.radians(theta))
        #         dist = math.acos(dist)
        #         dist = math.degrees(dist)
        #         miles = dist * 60 * 1.1515
        #         distance = miles * 1.609344
        #         distance = round(distance, 1)
        #         Orders.objects.filter(s_username = StoreUser).filter(id=k.id).update(dist_d_to_s = distance)
        #         AllDeliveries = Orders.objects.filter(order_completed = False).order_by('-date')
        #         Deliver_dict = {}
        #         Deliver_list = []
                
        #         for i in AllDeliveries:
        #             if i.d_response_status == True:
        #                 which_color = '#FF0000'
        #                 text='Accepted'
        #             else:
        #                 which_color = '#00FF00'
        #                 text='Accept'
                    
                    # if i.order_accept_status == 'accepted' and i.payment_status != 'not_responded':
                    #     if Shop.objects.filter(store_user=i.s_username).exists():
                    #         shopdata=Shop.objects.filter(store_user=i.s_username)[0]
                    #         storename = shopdata.name
                    #         store_address = shopdata.address
                    #         storecity = shopdata.city
                    #         storedistance = distance
                    #         date = i.order_accept_time
                    #         Deliver_dict= {
                    #             'store_name':storename,
                    #             'store_address':store_address,
                    #             'storecity':storecity,
                    #             'storedistance':storedistance,
                    #             'id':i.id,
                    #             'date':date,
                    #             'respondstatus':i.d_response_status,
                    #             'which_color':which_color,
                    #             'text':text,
                    #         }
                    #         Deliver_list.append(Deliver_dict)
        # pass
    
@login_required(redirect_field_name='next',login_url = '/login')
def DeliveryStatus(request,myid):
    if Orders.objects.filter(id=myid)[0].d_response_status == True:
        OrderId = Orders.objects.filter(id = myid)[0].orderid
        CurrrentOrder = Orders.objects.filter(id = myid)
        CurrentDict = {}
        StoreAddress = []
        Shop_obj = Shop.objects.all()
        for shop in Shop_obj:
            if shop.store_user == CurrrentOrder[0].s_username:
                CurrentDict = {
                    'store_name':shop.name,
                    'storeaddress':shop.address,
                    'OrderId':OrderId,
                }
                StoreAddress.append(CurrentDict)

        CustomerDict = {}
        CustomerAddress = []
        PersDetails = PersonalDetails.objects.filter(username=CurrrentOrder[0].c_username)[0]
        for detail in CurrrentOrder:
            CustomerDict={
            'c_name':str(PersDetails.fname) + str(" ") + str( PersDetails.lname),
            'c_address':detail.address,
            'orderid':OrderId,
            'amount':detail.price,
            }
            CustomerAddress.append(CustomerDict)

        #cash to be collected by delivery partner
        if CurrrentOrder[0].payment_completed == True:
            collect_cash = 0
        else:
            collect_cash=CurrrentOrder[0].total_amount

        if request.POST.get('reached_location'):
            reached_location = request.POST.get('reached_location')
            if reached_location == 'reached':
                CurrrentOrder.update(is_reached_store = True)
                TrackOrderChange(request,myid)
                
        if request.POST.get('reached_customer_location'):
            reached_location = request.POST.get('reached_customer_location')
            if reached_location == 'reached':
                CurrrentOrder.update(reached_location_status = True)
                TrackOrderChange(request,myid)
            
        
        if request.POST.get('collected_cash'):
            reached_location = request.POST.get('collected_cash')
            if reached_location == 'collected':
                CurrrentOrder.update(order_completed = True)
                TrackOrderChange(request,myid)
                return redirect('/get-delivery')
            
        if request.POST.get('customer_otp'):
            customer_otp = request.POST.get('customer_otp')
            if customer_otp != CurrrentOrder[0].customer_otp:
                pass
            else:
                TrackOrderChange(request,myid)
                CurrrentOrder.update(filled_otp=True)


        if request.FILES.get("parsel_image"):
            image_path = request.FILES.get("parsel_image")

            # image = NamedTemporaryFile()
            # image.write(urlopen(image_path).read())
            # image.flush()
            # image = File(image)
            # name = str(image.name).split('\\')[-1]
            # name += '.jpg' 

            ParselImage(image = image_path,order_id = myid).save()
            
    else:
        return redirect('/get-delivery')
    params = {'StoreAddress':StoreAddress,'CustomerAddress':CustomerAddress,
    'collect_cash':collect_cash,'CurrentDelivery':CurrrentOrder[0]}
    return render(request,'shops/delivery-status.html',params)

def OrderTracker(request,myid):
    data = Orders.objects.filter(id=myid)
    data = data[0]
    ShopName = Shop.objects.filter(store_user=data.s_username)[0].name
    DeliveryDate = data.date.strftime("%b-%d-%Y") 
    if PersonalDetails.objects.filter(username = data.d_username).exists():
        Obj = PersonalDetails.objects.filter(username = data.d_username)[0]
        DeliverName=str(Obj.fname) + str(" ") + str(Obj.lname)
        DeliverMobile = Obj.mob
        DeliveryDate = data.date.strftime("%b-%d-%Y") 
    else:
        DeliverName = None

        DeliverMobile = None
    images_data = ''        
    try:
        pres_id = data.images_id
        pres_data = Prescription.objects.filter(id=pres_id)
        pers_dict = {}
        for pers in pres_data:
            if pers.image1 != 'default.jpg':
                pers_dict[0] = pers.image1            
            if pers.image2 != 'default.jpg':
                pers_dict[1] = pers.image2 
            if pers.image3 != 'default.jpg':           
                pers_dict[2] = pers.image3 
            if pers.image4 != 'default.jpg':
                pers_dict[3] = pers.image4 
            if pers.image5 != 'default.jpg':
                pers_dict[4] = pers.image5
        images_data = []
        for img in range(len(pers_dict)):
            images_data.append(pers_dict[img])
    except:
        pass

    if data.order_accept_status == 'accepted':
        order_status = 'completed'
    else:
        order_status = " "

    if data.order_picked == True:
        picked_order = 'completed'
        
    else:
        picked_order = " "
    
    if data.order_picked == True:
        picked_order = 'completed'
        order_on_way = 'completed'
    else:
        picked_order = " "
        order_on_way = " " 
    
    if data.reached_location_status == True:
        order_reached = 'completed'
    else:
        order_reached = " "
    
    if data.order_completed == True:
        order_completed = 'completed'
    else:
        order_completed = " "
    
    # num_of_pers = len(pers_dict)
    inbox_items = data.inbox_items
    prod_dict = {}
    prod_list = []

    if len(data.items) > 1:
        product_list = json.loads(data.items)
        for i in product_list:
            product_name = product_list[i][1]
            product_qty = product_list[i][0]
            prod_dict = {
                'prod_name':product_name,
                'prod_qty':product_qty,
            }
            prod_list.append(prod_dict)

    Items_show = False
    items_dict = {}
    items_list = []
    if len(inbox_items) >= 1:
        Items_show = True
        inbox_items = json.loads(inbox_items)
        prod_len = 0
        for item in inbox_items:
            for j in item:
                prod_name=item[j][0] 
                prod_pack = item[j][1]
                qty = item[j][2]
                items_dict = {
                    'Product':prod_name,
                    'Pack':prod_pack,
                    'Quantity':qty,
                }
                prod_len = prod_len + len(prod_name)
                items_list.append(items_dict)

    # Payment mode
    if data.payment_status=='cod':
        pay_mode = 'Pay on Delivery'
    elif data.payment_status == 'card':
        pay_mode = 'Online'
    else:
        pay_mode = 'Incomplete'
    params = {'data':data,'prod_list':prod_list,'inbox_items':inbox_items,'myid':myid,'items_list':items_list, 
   'images_data':images_data,'ShopName':ShopName,'DeliverName':DeliverName,'Items_show':Items_show,
    'order_reached':order_reached,'order_on_way':order_on_way,'DeliverMobile':DeliverMobile,'DeliveryDate':DeliveryDate,
    'picked_order':picked_order,'order_status':order_status,'Order_Id':myid,'order_completed':order_completed,'pay_mode':pay_mode,
    }
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        url_path = 'app-view/user/home/order-tracker.html'
    except:          
        url_path = 'user/home/order-tracker.html'
    return render(request,url_path,params)

def TrackOrderChange(request,myid):
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_user==True:
        data = Orders.objects.filter(id=myid)
        data = data[0]
        DeliverName = None
        DeliverMobile = None
        
        if len(data.d_username) < 1:
            if PersonalDetails.objects.filter(username = data.d_username).exists():
                Obj = PersonalDetails.objects.filter(username = data.d_username)[0]
                DeliverMobile = Obj.mob
                DeliverName=str(Obj.fname) + str(" ") + str(Obj.lname)   
        else:
            DeliverName = data.d_username
            DeliverMobile = PersonalDetails.objects.filter(username=data.d_username)[0].mob
        if data.order_accept_status == 'accepted':
            request_accepted = 'active'
            order_status = 'active'
            if NotificationReminder.objects.filter(order_id = myid)[0].first == False:
                playsound('tones/notification_sound.mp3',False)
                NotificationReminder.objects.filter(order_id = myid).update(first = True)
        else:
            order_status = " "
            request_accepted = " "
        if data.order_picked == True:
            picked_order = 'active'
            order_on_way = "active" 
        else:
            picked_order = " "
            order_on_way = " " 
        if data.is_parsel_uploaded == True:
            if NotificationReminder.objects.filter(order_id = myid)[0].second == False:
                playsound('tones/notification_sound.mp3',False)
                NotificationReminder.objects.filter(order_id = myid).update(second = True)
        
            
        if data.reached_location_status == True:
            order_reached = 'active'
            if NotificationReminder.objects.filter(order_id = myid)[0].third == False:
                playsound('tones/notification_sound.mp3',False)
                NotificationReminder.objects.filter(order_id = myid).update(third = True)
        else:
            order_reached = " "

        if data.order_completed == True:
            order_completed = 'active'
            if NotificationReminder.objects.filter(order_id = myid)[0].fourth == False:
                playsound('tones/notification_sound.mp3',False)
                NotificationReminder.objects.filter(order_id = myid).update(fourth = True)
           
        else:
            order_completed = " "
        Order_objects = Orders.objects.filter(id=myid)
        data_dict = {}
        data_list = []

        request_accepted = {'request_accepted':request_accepted}
        picked_order = {"picked_order":picked_order}
        order_reached = {'order_reached':order_reached}
        order_completed = {'order_completed':order_completed}
        deliver_name = {'deliver_name':DeliverName}
        deliver_mob = {'deliver_mob':DeliverMobile}
    
        # data_list = json.dumps(data_list)
        return JsonResponse({'picked_order':picked_order,'order_reached':order_reached,'deliver_mob':deliver_mob,
        'order_completed':order_completed,'request_accepted':request_accepted,'DeliverName':DeliverName,'deliver_name':deliver_name,
        },safe=False)
    return render(request,'user/home/order-tracker.html')

def StoreResponse(request,myid):
    OrdersObj1 = Orders.objects.filter(id=myid)
    OrdersObj = OrdersObj1[0]  
    if request.FILES.get("inputbillimage"):
        image_path = request.FILES.get("inputbillimage") 
        OrdersObj1.update(is_bill_uploaded=True)
        StoreBill(image = image_path,order_id = myid).save()
        bill_uploaded = 'active'
        redirect(f'/store-order-response/{myid}')

    if request.POST.get('rejection_reason'):
        enteramount = request.POST.get('rejection_reason')
        if enteramount == '1':
            reason = 'Out of Stock'
        elif enteramount == '2':
            reason = 'Prescription is not clear'
        elif enteramount == '3':
            reason = 'Required doctors prescription'
        OrdersObj1.update(rejection_reason=reason)
        return redirect('/store-notifications')

    if request.POST.get('enteramount'):
        enteramount = request.POST.get('enteramount')
        OrdersObj1.update(store_amount=enteramount)
        AmountFilled = True
        filled_amount = 'active'
        redirect(f'/store-order-response/{myid}')

    if OrdersObj.store_amount == "":
        AmountFilled = False
        filled_amount = ''        
    else:
        AmountFilled = True
        filled_amount = 'active'

    if request.POST.get('process_completed'):
        if AmountFilled == True and OrdersObj.is_bill_uploaded == True:
            return redirect('/store-notifications')
    else:
        pass
    OrdersObj1 = Orders.objects.filter(id=myid)
    OrdersObj = OrdersObj1[0]

    if OrdersObj.is_bill_uploaded == True:
        bill_uploaded = 'active'
    else:
        bill_uploaded = ''

    params = {
        'OrdersObj':OrdersObj,'AmountFilled':AmountFilled,'bill_uploaded':bill_uploaded,
        'filled_amount':filled_amount,
        }
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        url_path = 'app-view/store/home/response.html'
    except:          
        url_path = 'store/home/response.html'
    return render(request,url_path,params)

def CustomerBilling(request,user_name,myid):
    ToalAmount = []
    if request.POST.get('payment_method'):
        value = request.POST.get('payment_method')
        customer_otp = GenerateOTP()
        if value == 'cash':
            time = datetime.now()
            Orders.objects.filter(id=myid).update(payment_status='cod',
            order_accept_time=time.strftime('%H:%M:%S'),customer_otp=customer_otp)
            DeliveryRequests(request,myid)
            return redirect('/')
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_user==True:
        bill_image_store = []
        if StoreBill.objects.filter(order_id=myid).exists():
            item_amount = Orders.objects.filter(id=myid)[0].store_amount
            delivery_charges = 10 
            GST = 5
            ToalAmount = int(item_amount) + delivery_charges + GST
            Orders.objects.filter(id=myid).update(total_amount = ToalAmount)
            bill_image_store1 =StoreBill.objects.filter(order_id=myid)
            for j in bill_image_store1:
                j.date = j.date  = j.date.strftime('%H:%M:%S')
                bill_image_store.append(j)
            bill_image_store = bill_image_store[-1]
            CurrentOrder = Orders.objects.filter(id = myid)
        
        pers_details = PersonalDetails.objects.get(username = str(request.user))
        customer_name = str(pers_details.fname) + str(pers_details.lname) 
        customer_mobile = pers_details.mob
        customer_email = pers_details.email
        order_amount = ToalAmount * 100
        order_currency = "INR"
        payment_order = client.order.create(dict(amount=order_amount,currency=order_currency,payment_capture =1))
        order_id = payment_order['id']
        Ob = Orders.objects.filter(id=myid).update(razorpay_order_id =order_id)
    context = {'api_key':RAZORPAY_API_KEY,'order_id':order_id,'customer_name':customer_name,
    'customer_mobile':customer_mobile,'customer_email':customer_email,
    'bill_image_store':bill_image_store,'ToalAmount':ToalAmount,'delivery_charges':delivery_charges,
    'GST':GST,}

    return render(request,'user/home/billing_page.html',context)
   
def GenerateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP
     
@login_required(redirect_field_name='next',login_url = '/login')
def RegisterDeliveryPartner(request):
    if request.method == 'POST':
        if request.POST.get('select_city'):
            select_city = request.POST.get('select_city')
                
           
        if request.FILES.get("adhar_doc"):
            adhar_doc = request.FILES.get("adhar_doc")
            
        if request.POST["src"]:
            image_path = request.POST["src"]  # src is the name of input attribute in your html file, this src value is set in javascript code
            image = NamedTemporaryFile()
            image.write(urlopen(image_path).read())
            image.flush()
            image = File(image)
            name = str(image.name).split('\\')[-1]
            name += '.jpg'  # store image in jpeg format
            image.name = name
        if request.POST.get('agree_conditions'):
            is_agree = request.POST.get('agree_conditions')

        DeliveryPartner(username=str(request.user),city=select_city,selfie = image,adhar =adhar_doc).save()
          
        try:
            obj.index('app-view') 
            return redirect('/app-view/home')  
        except:     
            return redirect('/')  
        
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        url_path = 'app-view/user/home/register-delivery-partner.html'
    except:          
        url_path = 'user/home/register-delivery-partner.html'
    return render(request,url_path)

@login_required(redirect_field_name='next',login_url = '/login')
def AddYourChemist(request):
    if request.method == 'POST':
        select_city = request.POST.get('select_city')
        storeowner = request.POST.get('storeowner')
        storename = request.POST.get('storename')
        storeaddress = request.POST.get('storeaddress')
        storemobile = request.POST.get('storemobile')
        storelicence = request.FILES.get("storelicence")
        storeadhar = request.FILES.get("storeadhar")
        storepan = request.FILES.get("storepan")
        storephoto = request.FILES.get("storephoto")
        Shop(name = storename,store_user=str(request.user),city=select_city,
            mobile=storemobile,address=storeaddress,pay_phone=storemobile,storelicence=storelicence,
            storeadhar=storeadhar,storepan=storepan,storephoto=storephoto).save()
        messages.success(request,'Thanks for joined with us.we will inform you very soon.')

        myurl = request.path
        obj = myurl.split('/')
        try:
            obj.index('app-view') 
            return redirect('/app-view/home')
        except:          
            return redirect('/')
    
    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        url_path = 'app-view/user/home/add-chemist.html'
    except:          
        url_path = 'user/home/add-chemist.html'
    return render(request,url_path)
# from . import utility
# class Utility(object):
#     def __init__(self,client = None):
#         self.client = client

client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
razorpay_client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))

@login_required(redirect_field_name='next',login_url = '/login')
def Payment(request): 
    order_amount = 30000
    order_currency = "INR"
    payment_order = client.order.create(dict(amount=order_amount,currency=order_currency,payment_capture =1))
    order_id = payment_order['id']
    Ob = Orders.objects.filter(id=71)[0]

    context = {'api_key':RAZORPAY_API_KEY,'order_id':order_id,'customer_name':'Tushar Patil',
    'customer_mobile':9148035748,'customer_email':'tusharspatil@gmail.com'}
    return render(request,'shops/payment.html',context)

@login_required(redirect_field_name='next',login_url = '/login')
def payment(request):
    final_price = 20000  
    amount = final_price
    currency = 'INR'
    razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = RAZORPAY_API_KEY
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    Orders.objects.filter(id=71).update(razorpay_order_id  = razorpay_order['id'])
    return render(request, 'shops/payment/paymentsummaryrazorpay.html',context=context)

def PaymentSuccess(request):
    return render(request, 'shops/payment/paymentsuccess.html')

@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature}
            # verify the payment signature.
            # result = razorpay_client.utility.verify_payment_signature(params_dict)
            util = razorpay.Utility(client)
            util.verify_payment_signature(params_dict)
            if util is None:
                amount = 20000  # Rs. 200
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    # render success page on successful caputre of payment
                    return render(request, 'shops/payment/paymentsuccess.html')
                except:
                    # if there is an error while capturing payment.
                    return render(request, 'shops/payment/paymentfailed.html')
            else:
 
                # if signature verification fails.
                return render(request, 'shops/payment/paymentfailed.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

@login_required(redirect_field_name='next',login_url = '/login')
def GetDelivery(request):
    if request.user.is_authenticated and user_type.objects.get(user=request.user).is_delivery==True:
        if request.POST.get('accept_btn'):
            del_response = request.POST.get('accept_btn')
            deliver = PersonalDetails.objects.filter(username = request.user)[0]
            delivername = str(deliver.fname) + str(deliver.lname)
            delivermobile = deliver.mob
            TrackOrderChange(request,del_response)
            Orders.objects.filter(id=int(del_response)).update(deliver_status = True,is_timeup = True,
            d_username=str(request.user))
            return redirect(f'/delivery-partner-response/{del_response}')
        GetDeliveryRequests(request)
    return render(request,'deliver/home/index.html')

def DeliveryPartnerResponse(request,myid):
    is_parsel_uploaded = ''
    is_order_confirmed = ''
    CurrrentOrder = Orders.objects.filter(id = myid)
    if request.POST.get('customer_otp'):
        customer_otp = request.POST.get('customer_otp')
        if customer_otp != CurrrentOrder[0].customer_otp:
            pass
        else:
            TrackOrderChange(request,myid)
            CurrrentOrder.update(filled_otp=True,is_reached_store=True)
            
    if request.FILES.get("parsel_image"):
            image_path = request.FILES.get("parsel_image")
            is_parsel_uploaded = 'active'
            is_order_confirmed = 'active'
            ParselImage(image = image_path,order_id = myid).save()
            CurrrentOrder.update(order_picked_status = True ,on_way_status = True,is_parsel_uploaded = True)
    
    if CurrrentOrder[0].order_picked_status == True:
        is_parsel_uploaded = 'active'
        is_order_confirmed = 'active'
    if request.POST.get('order_picked'):
        CurrrentOrder.update(order_picked_status = True ,on_way_status = True,is_parsel_uploaded = True,order_picked = True)
        TrackOrderChange(request,myid)

    if request.POST.get('reached_customer_location'):
        CurrrentOrder.update(reached_location_status = True)
        TrackOrderChange(request,myid)
    
    if request.POST.get('collected_cash'):
        CurrrentOrder.update(order_completed = True)
        TrackOrderChange(request,myid)
        return redirect('/get-delivery')    
        # redirect(f'/store-order-response/{myid}')

    if PersonalDetails.objects.filter(username = CurrrentOrder[0].c_username).exists():
        Obj = PersonalDetails.objects.filter(username = CurrrentOrder[0].c_username)[0]
        CustomerrName = str(Obj.fname) + str(" ") + str(Obj.lname)
    time = datetime.now()
    picked_time = time.strftime('%H:%M:%S')[:5]
    context = {'CurrrentOrder':CurrrentOrder[0],'is_order_confirmed':is_order_confirmed,'is_parsel_uploaded':is_parsel_uploaded,
    'CustomerrName':CustomerrName,'picked_time':picked_time}
    
    return render(request,'deliver/home/delivery-partner-response.html',context)  

previus_id = [] 
def GetDeliveryRequests(request):
    myid = None
    if Orders.objects.filter(payment_status ='cod').filter(is_timeup = False).exists():
        Orders_history = Orders.objects.filter(payment_status ='cod').filter(is_timeup = False)
        myid = Orders_history.last().id
        # Orders.objects.all().update(is_timeup = False,deliver_status=False,is_reached_store = False,is_parsel_uploaded = False)
        ord = Orders.objects.filter(id=myid)
        if ord[0].deliver_status == False and ord[0].deliver_status == False:
            if len(previus_id) > 10:
                previus_id.pop(0)
            data = {}
            if myid in previus_id:
                previus_id.append(myid)
            else:
                data = DeliveryRequests(request,myid)  
                previus_id.append(myid)
                return JsonResponse({'data':data})  

            time_completed = countdown(15)
            if time_completed is True:
                pass
                Orders.objects.filter(id=myid).update(is_timeup = True)
                DeliveryRequests(request,myid)
    return render(request,'deliver/home/index.html')
     
def countdown(t):
    time_completed = False
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        time.sleep(1)
        t -= 1 
    time_completed = True
    return time_completed

def DetectCurrentLocation(request):
    if request.POST.get('lon'):
        lon = request.POST.get('lon')
        lat = request.POST.get('lat')
        lat1 = float(lat)
        lon1 = float(lon)
        ob = Shop.objects.all()
        my_list = {}
        new_list = list()
        for i in ob:
            lon2 = float(i.lon)
            lat2 = float(i.lat)
            theta = lon1-lon2
            dist = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(theta))
            dist = math.acos(dist)
            dist = math.degrees(dist)
            miles = dist * 60 * 1.1515
            distance = miles * 1.609344
            distance = round(distance, 1)
            my_list= {
            'name':i.name,
            'city':i.city,
            'distance':distance,
            'address':i.address,
            'id':i.pk,
            }
            new_list.append(my_list)
        new_list.sort(key=lambda x: x["distance"])
        return JsonResponse({'context':new_list})
    return render(request,'user/home/select-location.html')

def Select_Location_Store(request):
    context = {}
    if request.POST.get('input_city_name'):
        city_input = request.POST.get('input_city_name')
        ob = Cities.objects.all()
        current_city_dict = {}
        current_city = list()
        for j in ob:
            if j.city_name.lower() == city_input.lower():
                current_city_dict = {
                'city_name':j.city_name,
                'state':j.state,
                }
                current_city.append(current_city_dict)  
        geolocator = Nominatim(user_agent="my_user_agent")
        country = 'india'
        city = city_input
        state = current_city[0]['state']
        placeholder_city = f'{city}, {state}'
        loc = geolocator.geocode(city+','+ country + ',' + state)
        lat1 = loc.latitude
        lon1 = loc.longitude        
        ob = Shop.objects.all()
        my_list = {}
        new_list = list()
        for i in ob:
            lon2 = float(i.lon)
            lat2 = float(i.lat)
            theta = lon1-lon2
            dist = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(theta))
            dist = math.acos(dist)
            dist = math.degrees(dist)
            miles = dist * 60 * 1.1515
            distance = miles * 1.609344
            distance = round(distance, 1)
            my_list= {
            'name':i.name,
            'city':i.city,
            'distance':distance,
            'address':i.address,
            'id':i.pk,
            }

            new_list.append(my_list)
        new_list.sort(key=lambda x: x["distance"])
        context = {'new_list':new_list}


    myurl = request.path
    obj = myurl.split('/')
    try:
        obj.index('app-view') 
        templates = 'app-view/user/home/select-location.html'
    except:          
        templates = 'user/home/select-location.html'
    return render(request,templates,context)

def GetData(request):
    if request.is_ajax():
        username = request.POST.get('data')
    return render(request,'user/home/index.html')

def Appview(request):
    templates = 'app-view/user/home/index.html'
    return render(request,templates)