from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SiteAdmin
from user.models import UserProfile
from vendor.models import Vendor
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password



def admin_login(request):
    if request.session.get('admin_id'):
        return redirect('admin_dashboard')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            admin = SiteAdmin.objects.get(username=username)
            if check_password(password, admin.password):
                request.session['admin_id'] = admin.id
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid password")
        except SiteAdmin.DoesNotExist:
            messages.error(request, "Admin not found")

    return render(request, 'login.html')

def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')


def admin_dashboard(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')
    return render(request, 'admin_dashboard.html')



def user_accounts(request):
    users = UserProfile.objects.all()
    return render(request, 'user_accounts.html', {'users': users})

def vendor_accounts(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor_accounts.html', {'vendors': vendors})



def delete_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    vendor.delete()  # this will also delete related tables if you use CASCADE
    return redirect('admin_vendor_accounts')