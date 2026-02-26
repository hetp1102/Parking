
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import transaction
from django.conf import settings
from .forms import SignupForm, LoginForm, BookingForm, ScanForm
from .models import Slot, Booking
import uuid, os
import qrcode

def home(request): return render(request,'home.html')

def signup_view(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            return redirect('login')
    else: form=SignupForm()
    return render(request,'signup.html',{'form':form})

def login_view(request):
    if request.method=='POST':
        form=LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else: form=LoginForm()
    return render(request,'login.html',{'form':form})

def logout_view(request):
    logout(request); return redirect('login')

@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user, active=True)
    form = BookingForm()
    message = None
    if request.method=='POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            slot = form.cleaned_data['slot']
            # atomic lock to prevent double booking
            with transaction.atomic():
                slot = Slot.objects.select_for_update().get(id=slot.id)
                if slot.is_occupied:
                    message = "❌ This slot is already booked."
                else:
                    slot.is_occupied=True; slot.save()
                    code = str(uuid.uuid4())
                    booking = Booking.objects.create(user=request.user, slot=slot, check_in=timezone.now(), code=code)
                    # generate QR
                    img = qrcode.make(code)
                    qr_path = os.path.join('qrs', f"{booking.id}.png")
                    full_path = os.path.join(settings.MEDIA_ROOT, qr_path)
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    img.save(full_path)
                    booking.qr_image = qr_path
                    booking.save()
                    return redirect('dashboard')
    return render(request,'dashboard.html',{'bookings':bookings,'form':form,'message':message})

def is_staff(user): return user.is_staff

@user_passes_test(is_staff)
def staff_dashboard(request):
    total = Slot.objects.count()
    occupied = Slot.objects.filter(is_occupied=True).count()
    free = total - occupied
    return render(request,'staff_dashboard.html',{'total':total,'occupied':occupied,'free':free})

@user_passes_test(is_staff)
def staff_scanner(request):
    message = None
    if request.method=='POST':
        code = request.POST.get('code')
        if code:
            try:
                booking = Booking.objects.get(code=code, active=True)
                booking.check_out = timezone.now()
                booking.active=False
                slot = booking.slot
                slot.is_occupied=False; slot.save()
                booking.save()
                message = "✅ Booking validated. Check-out successful!"
            except Booking.DoesNotExist:
                message = "❌ Invalid or already used QR."
    return render(request,'staff_scanner.html',{'message':message})

@user_passes_test(lambda u: u.is_superuser)
def admin_profile(request):
    return render(request,'admin_profile.html')
