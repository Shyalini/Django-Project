from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import Package, Booking


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_vendor = forms.BooleanField(required=False, label='Register as a vendor')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_vendor']

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            if self.cleaned_data['is_vendor']:
                vendor_group, created = Group.objects.get_or_create(name='Vendor')
                user.groups.add(vendor_group)
        return user


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['title', 'description', 'price', 'duration_days', 'expiry_date', 'image']

    def __init__(self, *args, **kwargs):
        super(PackageForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_people', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
