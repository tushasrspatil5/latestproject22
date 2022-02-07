from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    def __str__(self):
        return self.mobile

# from .views import request
class UserManager(BaseUserManager): 
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    def get_email(self):
        return self.email

# -----I will explain this part later. So let's keep it commented for now-------

class user_type(models.Model):
    is_store = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_delivery = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.is_user == True:
            return User.get_email(self.user) + " - is_user"
        elif self.is_store == True:
            return User.get_email(self.user) + " - is_store"
        elif self.is_delivery == True:
            return User.get_email(self.user) + " - is_delivery"

class Shop(models.Model):
    name = models.CharField(max_length=100)
    store_user = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()
    city = models.CharField(max_length=1000)
    mobile = models.CharField(max_length=200)
    address = models.CharField(max_length=1000)
    pay_phone = models.CharField(max_length=20,blank='')
    storelicence = models.ImageField(upload_to='images',default='default.jpg')
    storeadhar = models.ImageField(upload_to='images',default='default.jpg')
    storepan = models.ImageField(upload_to='images',default='default.jpg')
    storephoto = models.ImageField(upload_to='images',default='default.jpg')    
    def __str__(self):
        return self.name

class Cities(models.Model):
    """docstring for Cities"""
    city_name = models.CharField(max_length = 200)
    dist = models.CharField(max_length = 200)
    # country = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    def __str__(self):
        return self.city_name

class Image(models.Model):
    user = models.CharField(max_length=200)
    store_user = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now, blank=True)
    image = models.ImageField(upload_to='images')
    desc = models.TextField()
    def __str__(self):
        return str(self.user) 

class Prescription(models.Model):
    sender = models.CharField(max_length=200)
    reciver = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now, blank=True)
    image1 = models.ImageField(upload_to='images',default='default.jpg')
    image2 = models.ImageField(upload_to='images',default='default.jpg')
    image3 = models.ImageField(upload_to='images',default='default.jpg')
    image4 = models.ImageField(upload_to='images',default='default.jpg')
    image5 = models.ImageField(upload_to='images',default='default.jpg')
    desc = models.TextField()
    message = models.TextField()
    viewed = models.BooleanField(default = False)
    responed_status = models.CharField(max_length = 200, default = 'not_responded')
    def __str__(self):
        return str(self.sender) + '  ' + str(self.reciver)
    
class PersonalDetails(models.Model):
    """docstring for Cities"""
    fname = models.CharField(max_length = 200)
    lname = models.CharField(max_length = 200)
    username = models.CharField(max_length = 200)
    mob = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)
    city = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    address = models.CharField(max_length = 200)
    lat = models.CharField(max_length=200)
    lon = models.CharField(max_length=200)
    def __str__(self):
        return self.username

class Notification(models.Model):
    title = models.CharField(max_length = 200)
    message = models.TextField()
    viewed = models.BooleanField(default = False)
    sender = models.CharField(max_length = 200)
    date = models.DateTimeField(default=datetime.now, blank=True)
    reciver = models.CharField(max_length = 200)
    def __str__(self):
        return str(self.sender) + '  ' + str(self.reciver)
    def save(self, *args, **kwargs):
        # self.date = self.date.strftime('%H:%M:%S')
        return super(Notification, self).save(*args, **kwargs)

class Product(models.Model):    
    product_id=models.AutoField
    product_name = models.CharField(max_length=500)
    img_url1 = models.CharField(max_length = 500)
    img_url2 = models.CharField(max_length = 500)
    img_url3 = models.CharField(max_length = 500)
    img_url4 = models.CharField(max_length = 500)
    price=models.IntegerField()
    price_old =models.IntegerField()
    percent_off = models.CharField(max_length = 200)
    category= models.CharField(max_length=100)
    sub_category= models.CharField(max_length=100)
    brand = models.CharField(max_length= 100)
    manufacturer = models.CharField(max_length= 200)
    desc = models.TextField(default = "")
    use = models.CharField(max_length = 500,default = "")
    benefits = models.TextField(default = "")
    use_directions = models.TextField(default = "")
    safety_info = models.TextField(default = "")
    ingradients = models.TextField(default = "")
    pub_date=models.DateField()
    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        self.sub_category = self.sub_category.lower()
        self.category = self.category.lower()
        self.brand = self.brand.lower()
        return super(Product, self).save(*args, **kwargs)

class PlacedOrders(models.Model):
    customername = models.CharField(max_length = 200)
    username = models.CharField(max_length = 200)
    items = models.CharField(max_length = 2000)
    inbox_items = models.CharField(max_length = 5000)
    address = models.CharField(max_length = 2000)
    city = models.CharField(max_length = 2000)
    pincode = models.CharField(max_length = 2000)
    phone = models.CharField(max_length = 2000)
    price = models.IntegerField()
    store_status = models.BooleanField(default = False)
    deliver_status = models.BooleanField(default = False)
    order_picked_status = models.BooleanField(default = False)
    on_way_status = models.BooleanField(default = False)
    reached_location_status = models.BooleanField(default = False)
    order_completed = models.BooleanField(default = False)
    images = models.CharField(max_length = 3000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.customername


class GetDeliveries(models.Model):
    orderid = models.CharField(max_length=200)
    respondstatus = models.CharField(max_length=200)
    is_reached_store = models.BooleanField(default = False)
    is_reached_user = models.BooleanField(default = False)
    customername = models.CharField(max_length = 200)
    customeraddress = models.CharField(max_length=500)
    customermobile = models.CharField(max_length= 200)
    storeuser = models.CharField(max_length = 200)
    store_name = models.CharField(max_length=200)
    storeaddress = models.CharField(max_length = 500)
    storemobile = models.CharField(max_length = 200)
    storecity = models.CharField(max_length = 200)
    storedistance = models.CharField(max_length = 2000)
    delivername = models.CharField(max_length=200)
    deliverusername= models.CharField(max_length=200)
    delivermobile = models.CharField(max_length = 200)
    pricestatus = models.BooleanField(default = False)
    price = models.IntegerField()
    itemphoto = models.ImageField(upload_to='images',default='default.jpg')
    date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return str(self.storeuser) + str(self.deliverusername)  


class Orders(models.Model):
    orderid = models.CharField(max_length = 500)
    razorpay_order_id=models.CharField(max_length = 500)
    c_username = models.CharField(max_length = 200)
    s_username = models.CharField(max_length=200)
    images_id = models.CharField(max_length = 300)
    items = models.CharField(max_length = 2000)
    inbox_items = models.CharField(max_length = 5000)
    city = models.CharField(max_length = 2000)
    address = models.CharField(max_length = 2000)
    flat_no = models.CharField(max_length = 300)
    pincode = models.CharField(max_length = 2000)
    phone = models.CharField(max_length = 2000)
    store_notification_1 = models.TextField("")
    order_accept_status = models.CharField(max_length=200,default='not_responded')
    order_accept_time = models.CharField(max_length=200)
    rejection_reason = models.CharField(max_length=1000)
    user_notification_1 = models.TextField("")
    payment_status = models.CharField(max_length=100,default='not_responded') 
    payment_completed = models.BooleanField(default = False)
    price = models.CharField(max_length=2000)
    total_amount = models.CharField(max_length=2000)
    customer_otp = models.CharField(max_length=50)
    filled_otp=models.BooleanField(default = False)
    # dist_d_to_s = models.CharField(max_length=2000)
    
    d_username = models.CharField(max_length = 200) 
    deliver_status = models.BooleanField(default = False)
    is_timeup = models.BooleanField(default=False)
    order_picked = models.BooleanField(default = False)
    is_reached_store = models.BooleanField(default = False)
    itemphoto = models.ImageField(upload_to='images',default='default.jpg')
    order_picked_status = models.BooleanField(default = False)
    on_way_status = models.BooleanField(default = False)
    reached_location_status = models.BooleanField(default = False)
    order_completed = models.BooleanField(default = False)
    is_cancelled = models.BooleanField(default =False)
    is_bill_uploaded = models.BooleanField(default=False)
    bill_img_id = models.CharField(default='',max_length=200)
    
    parsel_img_id = models.CharField(default='',max_length=200)
    is_parsel_uploaded = models.BooleanField(default=False)
    store_amount = models.CharField(max_length=200,default="")
    
    date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.orderid

class StoreBill(models.Model):
    date = models.DateTimeField(default=datetime.now, blank=True)
    image = models.ImageField(upload_to='images')
    order_id = models.CharField(max_length=200)
    def __str__(self):
        return str(self.order_id) 

class ParselImage(models.Model):
    date = models.DateTimeField(default=datetime.now, blank=True)
    image = models.ImageField(upload_to='images')
    order_id = models.CharField(max_length=200)
    def __str__(self):
        return str(self.order_id) 

class NotificationReminder(models.Model):
    order_id = models.CharField(max_length=200)
    first = models.BooleanField(default = False)
    second = models.BooleanField(default = False)
    third = models.BooleanField(default = False)
    fourth = models.BooleanField(default = False)
    store_first = models.BooleanField(default = False)
    store_second = models.BooleanField(default = False)
    user_first = models.BooleanField(default = False)
    user_second = models.BooleanField(default = False)
    user_third = models.BooleanField(default = False)
    user_fourth = models.BooleanField(default = False)
    
    
class DeliveryPartner(models.Model):
    username = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=1000) 
    lat = models.CharField(max_length=500)
    lon = models.CharField(max_length=500)
    mobile = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now, blank=True)
    selfie = models.ImageField(upload_to='images')
    adhar = models.ImageField(upload_to='images')
    def __str__(self):
        return self.username

class SavedAddress(models.Model):
    date = models.DateTimeField(default=datetime.now, blank=True)
    username= models.CharField(max_length=300)
    landmark = models.CharField(max_length=1000)
    room_no = models.CharField(max_length=1000)
    def __str__(self):
        return str(self.username) 
