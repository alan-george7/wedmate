from django.contrib.auth.hashers import make_password, check_password
from .models import *
import random
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from vendor.models import *
from django.contrib.auth.decorators import login_required
from vendor.models import Booking




def user_register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        location = request.POST.get("location")
        username = request.POST.get("username")
        password = request.POST.get("password")
        re_password = request.POST.get("confirm_password")

        if password == re_password:
            if UserProfile.objects.filter(email=email).exists():
                messages.warning(request, "Email already exists.")
            elif UserProfile.objects.filter(username=username).exists():
                messages.warning(request, "Username already exists.")
            else:
                password = make_password(password)
                user = UserProfile.objects.create(
                    name=name,
                    mobile=mobile,
                    email=email,
                    location=location,
                    username=username,
                    password=password)
                user.save()

                messages.success(request, "User registered successfully.")
                return redirect('user_login')  # make sure this URL exists
        else:
            messages.warning(request, "Password mismatch.")

    return render(request, "user_registration.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        a = UserProfile.objects.filter(username=username).first()
        if a and check_password(password, a.password):
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"password":make_password(password)}
            )
            login(request, user)
            request.session['user_id'] = a.id
            print("User logged in with ID:", a.id)
            return redirect('user_dashboard')
        else:
            messages.warning(request, "Account not found")
    return render(request, "user_login.html")


def user_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if UserProfile.objects.filter(email=email).exists():
            def generate_otp():
                return random.randint(1000, 9999)

            otp = generate_otp()
            send_mail("OTP for Password Reset", f"Your OTP for forgot password verification is {otp}",
                      settings.EMAIL_HOST_USER, [email])
            request.session['otp'] = otp
            request.session['email'] = email
            request.session['time'] = str(datetime.now())
            return redirect('user_reset')
        else:
            messages.warning(request, "Account not Found")
    return render(request, "user_otp.html")


def user_reset(request):
    otp = request.session.get('otp')
    print(otp)
    email = request.session.get('email')
    send_time = request.session.get('time')
    send_time = datetime.strptime(send_time, "%Y-%m-%d %H:%M:%S.%f")
    current_time = datetime.now()
    duration = current_time - send_time
    print(duration)
    if request.method == "POST":
        otp1 = int(request.POST.get("otp"))
        # print(type(otp1))
        new_password = request.POST.get("password")
        re_password = request.POST.get("re_password")
        if new_password == re_password:
            if otp == otp1 and duration <= timedelta(minutes=5):
                user = UserProfile.objects.get(email=email)
                user.password=make_password(new_password)
                user.save()
                return redirect(user_login)
            elif otp == otp1 and duration > timedelta(minutes=5):
                messages.warning(request, "Time exceeded !!")
                return redirect('user_otp')
            else:
                messages.warning(request, "Invalid otp")
        else:
            messages.warning(request, "Password Mismatch")
    return render(request, "user_reset.html")


def user_dashboard(request):
    return render(request, "user_dashboard.html")



def user_logout(request):
    logout(request)
    return redirect(reverse("home"))


CATEGORY_MAP = {
    'venues': 'Venues',
    'photography': 'Photography',
    'makeup': 'Makeup',
    'catering': 'Catering',
    'decor': 'Decor',
    'music-dance': 'music-dance',
    'corporate-event': 'corporate Event',
}



def my_wishlist(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please login to view your wishlist.")
        return redirect('login_page')

    user = get_object_or_404(UserProfile, id=user_id)
    wishlist_items = Wishlist.objects.filter(user=user)
    return render(request, 'my_wishlist.html', {'wishlist_items': wishlist_items})


def show_venue(request):
    vendors = Vendor.objects.filter(business_type='Venues')
    selected_budget = request.GET.get('budget')

    if selected_budget == '25000_below':
        vendors = vendors.filter(budget_int__lte=25000)
    elif selected_budget == '50000_below':
        vendors = vendors.filter(budget_int__lte=50000)
    elif selected_budget == '100000_below':
        vendors = vendors.filter(budget_int__lte=100000)
    elif selected_budget == '100000_above':
        vendors = vendors.filter(budget_int__gt=100000)
    return render(request, "show_venue.html", {'vendors': vendors})


def show_photography(request):
    vendors = Vendor.objects.filter(business_type='Photography')
    selected_budget = request.GET.get('budget')

    if selected_budget == '25000_below':
        vendors = vendors.filter(budget_int__lte=25000)
    elif selected_budget == '50000_below':
        vendors = vendors.filter(budget_int__lte=50000)
    elif selected_budget == '100000_below':
        vendors = vendors.filter(budget_int__lte=100000)
    elif selected_budget == '100000_above':
        vendors = vendors.filter(budget_int__gt=100000)
    return render(request, "show_photography.html", {'vendors': vendors})


def show_makeup(request):
    vendors = Vendor.objects.filter(business_type='Makeup')
    selected_budget = request.GET.get('budget')

    if selected_budget == '25000_below':
        vendors = vendors.filter(budget_int__lte=25000)
    elif selected_budget == '50000_below':
        vendors = vendors.filter(budget_int__lte=50000)
    elif selected_budget == '100000_below':
        vendors = vendors.filter(budget_int__lte=100000)
    elif selected_budget == '100000_above':
        vendors = vendors.filter(budget_int__gt=100000)
    return render(request, "show_makeup.html", {'vendors': vendors})


def show_catering(request):
    vendors = Vendor.objects.filter(business_type='Catering')
    selected_budget = request.GET.get('budget')

    if selected_budget == '25000_below':
        vendors = vendors.filter(budget_int__lte=25000)
    elif selected_budget == '50000_below':
        vendors = vendors.filter(budget_int__lte=50000)
    elif selected_budget == '100000_below':
        vendors = vendors.filter(budget_int__lte=100000)
    elif selected_budget == '100000_above':
        vendors = vendors.filter(budget_int__gt=100000)
    return render(request, "show_catering.html", {'vendors': vendors})


def show_decor(request):
    vendors = Vendor.objects.filter(business_type='Decor')
    selected_budget = request.GET.get('budget')

    if selected_budget == '25000_below':
        vendors = vendors.filter(budget_int__lte=25000)
    elif selected_budget == '50000_below':
        vendors = vendors.filter(budget_int__lte=50000)
    elif selected_budget == '100000_below':
        vendors = vendors.filter(budget_int__lte=100000)
    elif selected_budget == '100000_above':
        vendors = vendors.filter(budget_int__gt=100000)
    return render(request, "show_decor.html", {'vendors': vendors})


def show_music(request):
    vendors = Vendor.objects.filter(business_type='Music/Dance')
    selected_budget = request.GET.get('budget')

    if selected_budget == '25000_below':
        vendors = vendors.filter(budget_int__lte=25000)
    elif selected_budget == '50000_below':
        vendors = vendors.filter(budget_int__lte=50000)
    elif selected_budget == '100000_below':
        vendors = vendors.filter(budget_int__lte=100000)
    elif selected_budget == '100000_above':
        vendors = vendors.filter(budget_int__gt=100000)
    return render(request, "show_music.html", {'vendors': vendors})


def show_events(request):
    vendors = Vendor.objects.filter(business_type='Corporate Event')
    selected_budget = request.GET.get('budget')

    if selected_budget == '25000_below':
        vendors = vendors.filter(budget_int__lte=25000)
    elif selected_budget == '50000_below':
        vendors = vendors.filter(budget_int__lte=50000)
    elif selected_budget == '100000_below':
        vendors = vendors.filter(budget_int__lte=100000)
    elif selected_budget == '100000_above':
        vendors = vendors.filter(budget_int__gt=100000)
    return render(request, "show_events.html", {'vendors': vendors})


def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    work_photos = VendorWorkPhoto.objects.filter(vendor=vendor)

    user = None
    is_wishlisted = False

    if request.user.is_authenticated:
        user = UserProfile.objects.filter(username=request.user.username).first()
        print("Found logged in user:", user)
        if user:
            is_wishlisted = Wishlist.objects.filter(user=user, vendor=vendor).exists()

    if request.method == 'POST' and user:
        comment = request.POST.get('comment')
        if comment:
            Review.objects.create(user=user, vendor=vendor, comment=comment)
            messages.success(request, "Review added successfully.")
            # return redirect(reverse('vendor_detail', args=[vendor_id]) + '#review-form')
            from_url = request.GET.get('from')
            if from_url:
                return redirect(f"{reverse('vendor_detail', args=[vendor_id])}?from={from_url}#review-form")
            else:
                return redirect(reverse('vendor_detail', args=[vendor_id]) + '#review-form')

    reviews = Review.objects.filter(vendor=vendor).order_by('-created_at')

    return render(request, 'vendor_detail.html', {
        'vendor': vendor,
        'work_photos': work_photos,
        'reviews': reviews,
        'user': user,
        'is_wishlisted': is_wishlisted,
        'previous_url': request.META.get('HTTP_REFERER', '/'),
    })


def user_bookings(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.warning(request, "Please log in first.")
        return redirect('user_login')

    user_profile = UserProfile.objects.get(id=user_id)
    bookings = Booking.objects.filter(user=user_profile)
    return render(request, 'user_bookings.html', {'bookings': bookings})


def cancel_booking(request, booking_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.warning(request, "Please log in first.")
        return redirect('user_login')

    booking = get_object_or_404(Booking, id=booking_id)

    if user_id != booking.user.id:
        messages.error(request, "You are not authorized to cancel this booking.")
        return redirect('user_bookings')

    booking.delete()
    messages.success(request, "Booking has been cancelled successfully!")

    return redirect('user_bookings')



def add_to_wishlist(request, vendor_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please login to add to wishlist.")
        return redirect('login_page')

    user = get_object_or_404(UserProfile, id=user_id)
    vendor = get_object_or_404(Vendor, id=vendor_id)

    Wishlist.objects.get_or_create(user=user, vendor=vendor)
    messages.success(request, "Vendor added to your wishlist.")
    from_url = request.GET.get('from')
    if from_url:
        return redirect(from_url)
    return redirect('vendor_detail', vendor_id=vendor_id)


def remove_from_wishlist(request, vendor_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please login to remove from wishlist.")
        return redirect('login_page')

    user = get_object_or_404(UserProfile, id=user_id)
    vendor = get_object_or_404(Vendor, id=vendor_id)

    Wishlist.objects.filter(user=user, vendor=vendor).delete()
    messages.success(request, "Vendor removed from your wishlist.")
    return redirect('my_wishlist')
