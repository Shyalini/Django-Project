from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
import razorpay
from .forms import CustomUserCreationForm, PackageForm, BookingForm
from .models import Package, Booking, Vendor
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings


# Check if User is Vendor
def is_vendor(user):
    return user.is_authenticated and user.groups.filter(name='Vendor').exists()


# User Registration
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            if form.cleaned_data.get('is_vendor'):
                vendor_group, created = Group.objects.get_or_create(name='Vendor')
                user.groups.add(vendor_group)
                Vendor.objects.create(user=user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('index')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# User Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('index')
        else:
            messages.error(request, 'Login failed. Please check your username and password.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# User Logout
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('login')


# Index View
def index(request):
    packages = Package.objects.filter(is_approved=True)
    return render(request, 'index.html', {'packages': packages})


# Package List View
def package_list(request):
    packages = Package.objects.filter(is_approved=True)
    return render(request, 'packages/package_list.html', {'packages': packages})


# Package Detail View
def is_vendor_or_staff(user):
    return user.is_authenticated and (user.is_staff or user.groups.filter(name='Vendor').exists())


@login_required
def package_detail(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if package.is_approved or is_vendor_or_staff(request.user):
        return render(request, 'packages/package_detail.html', {'package': package})


# Book Package View
@login_required
def book_package(request, pk):
    package = get_object_or_404(Package, pk=pk, is_approved=True)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.package = package
            booking.save()
            messages.success(request, 'Please pay the amount.')
            return redirect('payment', pk=booking.pk)
        else:
            messages.error(request, 'Booking failed. Please correct the errors.')
    else:
        form = BookingForm()
    return render(request, 'bookings/book_package.html', {'form': form, 'package': package})


@login_required
def payment(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    client = razorpay.Client(auth=("rzp_test_S7apYrGEoFx5gB", "ds4Gg3I5znmLpfXauTN7dOBW"))
    total_amount = float(booking.package.price) * booking.number_of_people * 100  # amount in paise

    try:
        payment = client.order.create({
            "amount": int(total_amount),
            "currency": "INR",
            "payment_capture": "1"
        })
        messages.success(request, 'Payment initiated successfully.')
    except Exception as e:
        messages.error(request, f'Payment initiation failed: {str(e)}')
        return redirect('book_package', pk=booking.package.pk)

    return render(request, 'payments/payment.html', {'payment': payment, 'booking': booking, 'total_amount': total_amount / 100})


# Payment Success View
@csrf_exempt
def payment_success(request):
    messages.success(request, 'Payment successful.')
    return redirect('index')


# Vendor Dashboard View
@login_required
@user_passes_test(is_vendor)
def vendor_dashboard(request):
    packages = Package.objects.filter(vendor=request.user.vendor)
    return render(request, 'vendors/vendor_dashboard.html', {'packages': packages})


# Manage Package View
@login_required
@user_passes_test(is_vendor)
def manage_package(request, pk=None):
    if pk:
        package = get_object_or_404(Package, pk=pk, vendor=request.user.vendor)
    else:
        package = None

    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            package = form.save(commit=False)
            package.vendor = request.user.vendor
            package.save()
            messages.success(request, 'Package saved successfully.')
            return redirect('vendor_dashboard')
        else:
            messages.error(request, 'Failed to save package. Please correct the errors.')
    else:
        form = PackageForm(instance=package)

    return render(request, 'vendors/manage_package.html', {'form': form})


# Admin Dashboard View
@staff_member_required
def admin_dashboard(request):
    packages = Package.objects.all()
    users = User.objects.all()
    vendors = Vendor.objects.all()
    return render(request, 'admin/admin_dashboard.html', {'packages': packages, 'users': users, 'vendors': vendors})


# Approve Package View
@staff_member_required
def approve_package(request, pk):
    package = get_object_or_404(Package, pk=pk)
    package.is_approved = True
    package.save()
    messages.success(request, 'Package approved successfully.')
    return redirect('admin_dashboard')


@csrf_exempt
def contact_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name', '')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Create the email message
        full_message = f"Name: {first_name} {last_name}\nEmail: {email}\n\nMessage:\n{message}"

        # Send email
        send_mail(
            'Contact Form Submission',
            full_message,
            settings.DEFAULT_FROM_EMAIL,
            ['tourpackages60@gmail.com'],
        )

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

    return render(request, 'company/contact.html')


def about_view(request):
    return render(request, 'company/about.html')
