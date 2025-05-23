from django import forms
from .models import *
from user.models import UserProfile


class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['profile_pic', 'name', 'organization', 'email', 'mobile', 'business_type', 'place', 'bio', 'budget', 'username']

class WorkPhotoForm(forms.ModelForm):
    class Meta:
        model = VendorWorkPhoto
        fields = ['photo']


class BookingForm(forms.ModelForm):
    event_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Booking
        fields = ['event_date', 'event_location', 'details']

    def __init__(self, *args, **kwargs):
        self.vendor = kwargs.pop('vendor', None)
        super(BookingForm, self).__init__(*args, **kwargs)

    def clean_event_date(self):
        event_date = self.cleaned_data['event_date']
        # Check if date already booked
        if Booking.objects.filter(vendor=self.vendor, event_date=event_date, status__in=['Pending', 'Accepted']).exists():
            raise forms.ValidationError("This date is already booked. Please select another date.")
        return event_date