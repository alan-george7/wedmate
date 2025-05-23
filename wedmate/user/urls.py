from django.urls import path
from .views import *
from vendor.views import *

urlpatterns = [
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('otp/', user_otp, name='user_otp'),
    path('reset/', user_reset, name='user_reset'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('logout/', user_logout, name='user_logout'),
    path('add-to-wishlist/<int:vendor_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', my_wishlist, name='my_wishlist'),
    path('show_venue/', show_venue, name='show_venue'),
    path('show_decor/', show_decor, name='show_decor'),
    path('show_music/', show_music, name='show_music'),
    path('show_events/', show_events, name='show_events'),
    path('show_makeup/', show_makeup, name='show_makeup'),
    path('show_catering/', show_catering, name='show_catering'),
    path('show_photography/', show_photography, name='show_photography'),
    path('vendor/<int:vendor_id>/', vendor_detail, name='vendor_detail'),
    path('vendor/<int:vendor_id>/add-to-wishlist/', add_to_wishlist, name='add_to_wishlist'),
    path('vendor/<int:vendor_id>/book/', create_booking, name='create_booking'),
    path('bookings/', user_bookings, name='user_bookings'),
    path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
path('remove-from-wishlist/<int:vendor_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]
