"""newproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path
from customuser import views,customers
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # for store owner
    path('ajax/foo/<int:myid>', customers.upload, name='upload'),
    path('get_users_notifications',views.get_users_notifications,name = 'get_users_notifications'),
    path('show/notifications/<str:user_name>/request',views.show_notifications,name='show_notifications'),
    path('notification_view/',views.notification_view,name="notification_view"),
    path('store-notifications',views.StoreNotifications,name='store-notifications'),
    path('users-notifications',customers.UsersNotifications,name='users-notifications'),
    # path('store-notification/details/<str:current_user>',views.notification_view_details,name="notification_view_details"),
    path('store-list',views.StoreList,name='store-list'),
    path('store-notification/details/<str:current_user>/<int:myid>',views.notification_view_details,name="notification_view_details"),
    path('users-notification/details/<str:current_user>/<int:myid>',views.UsersNotificationDetails,name="UsersNotificationDetails"),
    path('admin/', admin.site.urls), 
    path("",views.home,name='home'),
    # path('signup',views.signup,name='signup'),
    path('search-location/',views.search_results, name='search-location'),
    path('search-products/',views.SearchProducts,name='search-products'),
    path('list-stores',views.list_stores, name="list_stores"),
    path('medical_store_view/<int:myid>',customers.medical_store_view, name = 'medical_store_view'),
    path('store-view/<int:myid>/<str:st_name>/<str:st_dist>',customers.medical_store_view, name='medical_store_view'),
    path('medical-store-view/<int:myid>/upload-prescriptions',customers.upload, name = 'medical_store_view'),
    path('upload',customers.upload,name='upload'),      
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('logout', views.handelLogout, name="handleLogout"),
    path('login', views.login_attempt, name="handleLogin"),
    path('user-login',views.UserLogin,name="UserLogin"),
    # path('forget-password',views.ForgetPassword,name="forget-password"),
    path('forget-password/' ,views.ForgetPassword , name="forget_password"),
    path('change-password/<token>/',views.ChangePassword , name="change_password"),
    path('upload-prescriptions',views.UploadPrescriptions,name = "upload-prescriptions"),
    path('checkout',customers.CheckOut,name='checkout'),
    path('myorders',customers.MyOrders,name='myorders'),
    path('product-view/<int:myid>',views.ProductView,name='ProductView'),
    path('get-delivery',views.GetDelivery,name='get-delivery'),
    path('tracking-order-status/<int:myid>',views.DeliveryStatus,name='tracking-order-status'),
    # path('upload-users-selfie', views.image_upload, name='image_upload'),
    path('order-tracker/<int:myid>',customers.OrderTracker,name='order-tracker'),
    path('tracker-order-change/<int:myid>',views.TrackOrderChange,name='TrackOrderChange'),
    path('store-order-response/<int:myid>',views.StoreResponse,name='store-order-response'), 
    path('customers-billing-page/<str:user_name>/<int:myid>',customers.CustomerBilling,name='CustomerBilling'),
    path('get-delivery-requests',views.DeliveryRequests,name='get-delivery-requests'),
    path('check-all-notifacations',views.CheckNOfitication,name='check-all-notifacations'),
    path('register-delivery-partner',views.RegisterDeliveryPartner, name='register-delivery-partner'),
    path('add-your-chemiest',views.AddYourChemist,name='add-your-chemiest'),
    path('make-payment',views.Payment,name='make-payment'),
    path('paymenthandler/',views.handlerequest,name='handlerequest'),
    path('payment-success',views.PaymentSuccess,name='payment-success'),

    # Profile ---
    path('users/<str:fname>-<str:lname>/profile',views.MyProfile,name='MyProfile'), 
    path('users/myprofile',views.NewMyProfile,name='NewMyProfile'),
    path('my-addresses',customers.MyAddresses,name='app-view/my-addresses'),
    path('users/<str:fname>-<str:lname>/profile/my-addresses',customers.MyAddress,name='MyAddress'),
    path('delivery-partner-response/<int:myid>',views.DeliveryPartnerResponse,name='DeliveryPartnerResponse'),
    path('googlemaps',views.GoogleMap,name='googlemaps'),
    # path('sample',views.sample,name='sample'),
    path('get-new-delivery',views.GetDeliveryRequests,name='get-new-delivery'),
    path('new-login',views.login_attempt , name="login"),
    path('register' , views.register , name="register"),
    path('otp' , views.otp , name="otp"),
    path('login-otp',views.login_otp , name="login_otp") ,
    path("logout/", views.handelLogout, name="logout"),
    # New Urls
    path('home/select-location',customers.Select_Location_Store,name='Select_Location_Store'),
    path('detect-users-location',views.DetectCurrentLocation,name='DetectCurrentLocation'),
    path('get-data',views.GetData,name='get-data'),

    # Application View 
    # For User
    path('app-view/home',views.Appview,name='app-view/home'),
    path('app-view/home/select-location',customers.Select_Location_Store,name='Select_Location_Store'),
    path('app-view/store-view/<int:myid>/<str:st_name>/<str:st_dist>',customers.medical_store_view, name='medical_store_view'),
    path('app-view/medical-store-view/<int:myid>/upload-prescriptions',customers.upload, name = 'medical_store_view'),
    path('app-view/checkout',customers.CheckOut,name='checkout'),
    path('app-view/users-notifications',customers.UsersNotifications,name='app-view/notifications'),
    path('app-view/users-notification/details/<str:current_user>/<int:myid>',views.UsersNotificationDetails,name="UsersNotificationDetails"),
    path('app-view/myorders',customers.MyOrders,name='app-view/myorders'),
    path('app-view/order-tracker/<int:myid>',customers.OrderTracker,name='app-view/order-tracker'),
    path('app-view/user/profile',views.AppMyProfile,name='MyProfile'),
    path('app-view/my-addresses',customers.MyAddresses,name='app-view/my-addresses'),
    path('app-view/register-delivery-partner',views.RegisterDeliveryPartner, name='register-delivery-partner'),
    path('app-view/add-your-chemiest',views.AddYourChemist,name='add-your-chemiest'),
    path('app-view/customers-billing-page/<str:user_name>/<int:myid>',customers.CustomerBilling,name='CustomerBilling'),

    #For Store
    path('app-view/store-notifications',views.StoreNotifications,name='store-notifications'),
    path('store-notification/details/<str:current_user>/<int:myid>',views.notification_view_details,name="notification_view_details"),
    path('app-view/store-notification/details/<str:current_user>/<int:myid>',views.notification_view_details,name="notification_view_details"),
    path('app-view/store-order-response/<int:myid>',views.StoreResponse,name='store-order-response'),
    # path('home/callback',views.callback,name='callback'),

    #For Delivery-Partner
    path('app-view/get-delivery-requests',views.GetDeliveryNew,name='get-delivery-requests'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
