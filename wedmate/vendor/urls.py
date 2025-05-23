from django.urls import path
from .views import *

urlpatterns = [
    path("register/", vendor_register, name="vendor_register"),
    path("login/", vendor_login, name="vendor_login"),
    path("otp/", vendor_otp, name="vendor_otp"),
    path("reset/", vendor_reset, name="vendor_reset"),
    path("dashboard/", vendor_dashboard, name="vendor_dashboard"),
    path("logout/", vendor_logout, name="vendor_logout"),
    path("payment/", vendor_payment, name="vendor_payment"),
    path('profile/', view_vendor_profile, name='view_vendor_profile'),
    path('profile/edit/', edit_vendor_profile, name='edit_vendor_profile'),
    path('delete-work-photo/<int:photo_id>/', delete_work_photo, name='delete_work_photo'),
    path('vendor/booking-requests/', booking_requests, name='booking_requests'),
    path('booking-request/accept/<int:booking_id>/', accept_booking, name='accept_booking'),
    path('booking-request/reject/<int:booking_id>/', reject_booking, name='reject_booking'),
    path('vendor/view-bookings/', vendor_view_bookings, name='vendor_view_bookings'),

]
