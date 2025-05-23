from audioop import reverse
from main.views import *
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from .forms import *
from user.models import UserProfile



def vendor_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        business_type = request.POST.get('business_type')
        place = request.POST.get('place')
        organization = request.POST.get('organization')
        profile_pic = request.FILES.get('profile_pic')
        bio = request.POST.get('bio')
        budget = request.POST.get('budget')
        password = request.POST.get('password')
        re_password = request.POST.get('confirm_password')

        if password == re_password:
            if Vendor.objects.filter(email=email).exists():
                messages.warning(request, "Email already exists.")
            elif Vendor.objects.filter(username=username).exists():
                messages.warning(request, "Username already exists.")
            else:
                password = make_password(password)
                budget_int = int(budget) if budget else 0
                vendor= Vendor.objects.create(
                    name=name,
                    email = email,
                    mobile = mobile,
                    business_type = business_type,
                    place = place,
                    username = username,
                    password = password,
                    profile_pic = profile_pic,
                    bio = bio,
                    budget = budget,
                    budget_int=budget_int,
                    organization = organization
                )
                vendor.save()
                request.session['vendor_id'] = vendor.id
                return redirect(vendor_payment)
        else:
            messages.warning(request, "Password mismatch.")
    return render(request, "vendor_register.html")


def vendor_payment(request):
    vendor_id = request.session.get('vendor_id')
    if not vendor_id:
        messages.warning(request, "Session expired. Please register again.")
        return redirect(vendor_register)

    vendor = Vendor.objects.get(id=vendor_id)

    if request.method == 'POST':
        card_name = request.POST.get('card_name')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        VendorPayment.objects.create(
            vendor=vendor,
            cardholder_name=card_name,
            card_number=card_number,
            expiry_date=expiry_date,
            cvv=cvv
        )
        messages.success(request, "Payment successful! You can now log in.")
        return redirect(vendor_login)

    return render(request, "vendor_payment.html", {'vendor': vendor})


def vendor_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        a = Vendor.objects.filter(username=username).first()
        if a and check_password(password, a.password):
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"password": make_password(password)}
            )
            login(request, user)
            request.session['vendor_id'] = a.id
            return redirect(vendor_dashboard)
        else:
            messages.warning(request, "Invalid credentials or payment not completed.")
    return render(request, "vendor_login.html")


def vendor_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if Vendor.objects.filter(email=email).exists():
            otp = random.randint(1000, 9999)
            send_mail("Vendor OTP", f"Your OTP is {otp}", settings.EMAIL_HOST_USER, [email])

            request.session['vendor_otp'] = otp
            request.session['vendor_email'] = email
            request.session['vendor_otp_time'] = str(datetime.now())
            return redirect('vendor_reset')
        else:
            messages.warning(request, "Email not registered")
    return render(request, "vendor_otp.html")


def vendor_reset(request):
    otp_sent = request.session.get('vendor_otp')
    email = request.session.get('vendor_email')
    send_time_str = request.session.get('vendor_otp_time')
    send_time = datetime.strptime(send_time_str, "%Y-%m-%d %H:%M:%S.%f")
    duration = datetime.now() - send_time

    if request.method == "POST":
        otp_entered = int(request.POST.get("otp"))
        new_password = request.POST.get("password")
        re_password = request.POST.get("re_password")

        if new_password != re_password:
            messages.warning(request, "Passwords do not match")
        elif otp_entered != otp_sent:
            messages.warning(request, "Invalid OTP")
        elif duration > timedelta(minutes=5):
            messages.warning(request, "OTP expired")
            return redirect('vendor_otp')
        else:
            vendor = Vendor.objects.get(email=email)
            vendor.password = make_password(new_password)
            vendor.save()
            messages.success(request, "Password reset successfully")
            return redirect('vendor_login')

    return render(request, "vendor_reset.html")


def vendor_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect(reverse('home'))


def vendor_dashboard(request):
    vendor_id = request.session.get('vendor_id')
    vendor = get_object_or_404(Vendor, id=vendor_id)
    return render(request, "vendor_dashboard.html", {'vendor': vendor})



@login_required
def view_vendor_profile(request):
    vendor_id = request.session.get('vendor_id')

    if not vendor_id:
        messages.error(request, "Please log in first.")
        return redirect('vendor_login')

    vendor = get_object_or_404(Vendor, id=vendor_id)
    work_photos = VendorWorkPhoto.objects.filter(vendor=vendor)
    if request.method == 'POST' and request.FILES.get('work_photo'):
        work_photo = request.FILES['work_photo']
        VendorWorkPhoto.objects.create(vendor=vendor, photo=work_photo)
        return redirect('view_vendor_profile')

    context = {
        'vendor': vendor,
        'work_photos': work_photos
    }

    return render(request, 'view_profile.html', {
        'vendor': vendor,
        'work_photos': work_photos
    })



@login_required
def edit_vendor_profile(request):
    vendor = Vendor.objects.get(username=request.user.username)
    work_photos = VendorWorkPhoto.objects.filter(vendor=vendor)

    if request.method == 'POST':
        profile_form = VendorProfileForm(request.POST, request.FILES, instance=vendor)

        if profile_form.is_valid():
            profile_form.save()


            for file in request.FILES.getlist('work_photos'):
                VendorWorkPhoto.objects.create(vendor=vendor, photo=file)

            return redirect('view_vendor_profile')
    else:
        profile_form = VendorProfileForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'work_photos': work_photos,
    }
    return render(request, 'edit_profile.html', context)



@login_required
def delete_work_photo(request, photo_id):
    photo = get_object_or_404(VendorWorkPhoto, id=photo_id)
    vendor = photo.vendor
    if vendor.username == request.user.username:
        photo.delete()
    return redirect('edit_vendor_profile')




def create_booking(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    user = get_object_or_404(UserProfile, id=request.session['user_id'])

    booked_dates = Booking.objects.filter(
        vendor=vendor,
        status__in=['Pending', 'Accepted']
    ).values_list('event_date', flat=True)


    booked_dates = [date.strftime("%Y-%m-%d") for date in booked_dates]

    if request.method == 'POST':
        form = BookingForm(request.POST, vendor=vendor)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.vendor = vendor
            booking.user = user
            booking.save()
            if request.method == 'POST':
                booking.save()
                messages.success(request, 'Booking successful!')
                return redirect('user_dashboard')
    else:
        form = BookingForm(vendor=vendor)

    return render(request, 'create_booking.html', {
        'form': form,
        'vendor': vendor,
        'booked_dates': booked_dates
    })




def booking_requests(request):
    vendor_id = request.session.get('vendor_id')
    vendor = get_object_or_404(Vendor, id=vendor_id)

    bookings = Booking.objects.filter(vendor=vendor, status='Pending')

    return render(request, 'booking_requests.html', {'vendor': vendor, 'bookings': bookings})


def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    booking.status = 'Accepted'
    booking.save()

    messages.success(request, 'Booking accepted successfully!')
    return redirect('booking_requests')


def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    booking.status = 'Rejected'
    booking.save()

    messages.success(request, 'Booking rejected successfully!')
    return redirect('booking_requests')


def vendor_view_bookings(request):
    vendor_id = request.session.get('vendor_id')
    if not vendor_id:
        messages.warning(request, "Please log in as vendor first.")
        return redirect('vendor_login')

    vendor = get_object_or_404(Vendor, id=vendor_id)

    bookings = Booking.objects.filter(vendor=vendor, status='Accepted')

    return render(request, 'vendor_view_bookings.html', {'bookings': bookings})