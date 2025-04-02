from django.shortcuts import render, redirect
from .models import parkuser,parkspace, parkhistory
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate
from .forms import SignUpForm, add_book
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import parkhistorySerializer, parkspaceSerializer
from django.shortcuts import get_object_or_404
import random
from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework import status


def home(request):
    return render(request,"parking_management/home.html")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'parking_management/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'parking_management/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect("home")


@login_required(login_url='home')
@api_view(['GET'])
def spaces_list(request):
    spaces = parkspace.objects.all()
    if request.user.role == 'ADMIN':
        serializer = parkspaceSerializer(spaces,many=True)
        return render(request, 'parking_management/spaces_list.html', {'spaces': spaces}, status=status.HTTP_200_OK)
    else:
        a = []
        for space in spaces:
            a.append({
                "Level" : space.Level,
                "TWA" : "available" if space.TWA > 0 else "Not-available",
                "FWA" : "available" if space.FWA > 0 else "Not-available",
            })
        return render(request, 'parking_management/spaces_list.html', {'spaces': a}, status=status.HTTP_200_OK)


@login_required(login_url='home')
# @api_view(['POST'])
def add_booking(request):
    context = {}
    book = add_book(request.POST or None)
    if book.is_valid():
        category = book.cleaned_data['Type']
        number = book.cleaned_data['VehicleNumber']
        level = book.cleaned_data['Level']
        try:
            space = get_object_or_404(parkspace, Level=level)
            slots_assigned = parkhistory.objects.filter(Level=level,Type=category).values_list("Lot",flat=True)
            slots_remaining = list(set(range(1,21)) - set(slots_assigned))
            if slots_remaining==[]:
                return HttpResponse("No Available Slots")
            assign = random.choice(slots_remaining)
            if assign == 0:
                return HttpResponse("No Available Slots")
            elif category == 'TWA':
                space.TWA -= 1
            elif category == 'FWA':
                space.FWA -= 1
            else:
                return HttpResponse({"error":"Invalid Entry"})
            space.save()
            booking = parkhistory.objects.create(
                Level=level,
                Type=category,
                VehicleNumber=number,
                Lot=assign,
            )
            serializer = parkhistorySerializer(booking)
            out = serializer.data
            out["mine"] = request.user
            return render(request, 'parking_management/add_booking.html', out)
        except:
            return HttpResponse("Level Doesnot Exist")
    context['form'] = book
    return render(request, "parking_management/bookin.html", context)



@login_required(login_url='home')
# @api_view(['POST'])
def assign(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        book = parkhistory.objects.filter(VehicleNumber=number).first()
        if book:
            book.Intime = timezone.now()
            book.save()
            out = parkhistorySerializer(book).data
            out["mine"] = request.user
            return render(request, 'parking_management/add_booking.html', out)
        else:
            return HttpResponse(
                "<h3>vehicle Doesnot Exist, Please book it first from home</h3>"
                "<h3><a href=../booking>Book Now</a></h3>"
                )
    return render(request, 'parking_management/final.html')

@login_required(login_url='home')
# @api_view(['POST'])
def unlock(request):
    if request.method == 'POST':
        number = request.POST.get("number")
        book = parkhistory.objects.filter(VehicleNumber=number).first()
        if book:
            space = get_object_or_404(parkspace, Level=book.Level)
            if book.Type == 'TWA':
                space.TWA += 1
            else :
                space.FWA += 1
            space.save()
            book.Outtime = timezone.now()
            book.Fee = (book.Outtime - book.Intime).total_seconds() * 0.01
            book.Lot = 0
            book.save()
            out = parkhistorySerializer(book).data
            out["mine"] = request.user

            return render(request, 'parking_management/add_booking.html', out)
        else:
            return HttpResponse("vehicle Doesnot Exist")
    return render(request, 'parking_management/final.html')


@login_required(login_url='home')
# @api_view(['POST'])
def cancel(request):
    if request.method == 'POST':
        number = request.POST.get("number")
        final = parkhistory.objects.filter(VehicleNumber=number).first()
        if final:
            space = get_object_or_404(parkspace, Level=final.Level)
            if final.Type == 'TWA':
                space.TWA += 1
            else :
                space.FWA += 1
            space.save()
            parkhistory.objects.filter(VehicleNumber=number).delete()
            return redirect('home')
        else:
            return HttpResponse("vehicle Doesnot Exist")
    return render(request, 'parking_management/final.html')