from django.contrib.auth.models import User, auth
from django.contrib import messages
import pandas as pd
import csv
import os
import datetime
from .predict import prod
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *

from twilio.rest import Client as Clientelle
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json
from django.templatetags.static import static
import base64
import numpy as np
# Create your views here.

account_sid = 'ACe5b4d5166816d11c745a003dd9a282b6'
auth_token = 'ba5ba937994122f7017ff2fd6350d79f'
clientelle = Clientelle(account_sid, auth_token)

def call():
    cally = clientelle.calls.create(
                        twiml='<Response><Say>Please Check the platform there is a client who is in distress!</Say></Response>',
                        to='+263784873574',
                        from_='+18154966506'
                    )

    print(cally.sid)

def calling(request):
    #call()
    return render(request, 'calling_patient.html')


def home(request):

    user = request.user

    comp = Company.objects.get(user=user)



    appointments = Appointment.objects.all().filter(facility=comp)

    appointmentCount = appointments.count()

    print(appointmentCount)

    sales = Sales.objects.all().filter(user=user)

    earning = 0

    for sale in sales:

        earning = earning + sale.treatment.cost

    print(earning)

    salesCount = sales.count()

    context = {'user': user, 'earning' : earning, 'salesCount': salesCount, 'appointmentCount':appointmentCount }
    
    return render(request, 'index.html', context)

def patient_home(request):

    user = request.user

    context = {'user': user}
    
    return render(request, 'index.html', context)

def admin(request):
    return redirect('admin/')

def logout(request):
	
	auth.logout(request)
	
	return redirect('login')

def medical_record_alter(request):
    if request.method == 'POST':

        patient = request.POST['patient']

        record = MedicalRecord.objects.get(pk=patient)

        temp = request.POST['temp']

        bp = request.POST['bp']

        admission = False

        discharged = False

        data = request.POST.items()


        for keys, values in data:

            if keys == "admission":

                admission = request.POST['admission']

            if keys == "discharged":

                discharged = request.POST['discharged']


        

        diseases = request.POST['diseases']

        notes = request.POST['notes']

        prescriptions = request.POST['prescriptions']

        doa = request.POST['doa']

        dod = request.POST['dod']

        if doa == "":
            doa = None

        if dod == "":
            dod = None

        user = request.user


        if admission == "on":
            admission = True
        else:
            admission = False

        if discharged == "on":
            discharged = True
        else:
            discharged = False

        medicRecord = MedicalRecord.objects.all().filter(pk=patient).update(user=user, admitted=admission, dateOfAdmission=doa, discharged=discharged, dateOfDischarge=dod, temp=temp, disease=diseases, notes=notes, bpNo=bp, prescriptions=prescriptions)

        messages.info(request, 'Record Successfully Updated!!')

        return redirect('medical_record')

def medical_record(request):
    if request.method == 'POST':

        patient = request.POST['patient']

        temp = request.POST['temp']

        treatCount = request.POST['treatCount']

        treatCount = int(treatCount)




        bp = request.POST['bp']

        admission = False

        discharged = False

        data = request.POST.items()


        for keys, values in data:

            if keys == "admission":

                admission = request.POST['admission']

            if keys == "discharged":

                discharged = request.POST['discharged']


        

        diseases = request.POST['diseases']

        notes = request.POST['notes']

        prescriptions = request.POST['prescriptions']

        doa = request.POST['doa']

        dod = request.POST['dod']

        if doa == "":
            doa = None

        if dod == "":
            dod = None

        user = request.user

        patent = Patient.objects.get(pk=patient)

        

        if admission == "on":

            admission = True

        else:
            admission = False

        if discharged == "on":

            discharged = True

        else:

            discharged = False

        medicRecord = MedicalRecord.objects.create(user=user, patient=patent, admitted=admission, dateOfAdmission=doa, discharged=discharged, dateOfDischarge=dod, temp=temp, disease=diseases, notes=notes, bpNo=bp, prescriptions=prescriptions)

        medicRecord.save();

        for treat in range(1, treatCount):

            treatCount = request.POST['treatment-'+str(treat)]

            treatment = Treatment.objects.get(pk=treatCount)

            sale = Sales.objects.create(user=user, patient=patent, record=medicRecord, treatment=treatment)

            sale.save();

        return redirect('medical_record')

    else:

        user = request.user

        records = MedicalRecord.objects.all().filter(user=user)


        context = {'records': records, 'user': user}

        return render(request, 'medical_records.html', context)

def patient_record(request):
    if request.method == 'POST':
        user = request.user

        natID = request.POST['natID']

        patent = Patient.objects.get(nat_id=natID)

        records = MedicalRecord.objects.all().filter(patient=patent.pk)

        patentsp = PatientSpecial.objects.get(patient=patent)

        current_date = datetime.datetime.now()

        patentAge = current_date.year - patent.dob.year
        
        context = {'patient': patent, 'patientsp': patentsp, 'patientAge': patentAge, 'records': records, 'user': user}

        return render(request, 'patient_record_view.html', context)

    else:

        user = request.user

        context = {'user': user}

        return render(request, 'patient_record_view.html', context)

def medical_recordID(request):

    if request.method == 'POST':
        user = request.user

        records = MedicalRecord.objects.all().filter(user=user)

        natID = request.POST['natID']
                
        treatments = Treatment.objects.all()

        patent = Patient.objects.get(nat_id=natID)

        patentsp = PatientSpecial.objects.get(patient=patent)

        current_date = datetime.datetime.now()

        patentAge = current_date.year - patent.dob.year
        
        context = {'patient': patent, 'treatments': treatments, 'patientsp': patentsp, 'patientAge': patentAge, 'records': records, 'user': user}

        return render(request, 'medical_records.html', context)

    else:

        return redirect('medical_record')

def subscriptionsPay(request):

    user = request.user

    payment_date = datetime.datetime.now()

    expiry_date = payment_date.replace(month = payment_date.month + 1)


    subscrips = Subscriptions.objects.all().filter(user=request.user)

    for subscrip in subscrips:

        check = subscrip.expiry_date.month - payment_date.month

        if check >= 1:

            print(subscrip.expiry_date.month)

            print(payment_date.month)

            messages.info(request, 'Your subscription hasnt expired yet')

            return redirect('subscriptions')




    subs = Subscriptions.objects.create(user=user, payment_date=payment_date, expiry_date=expiry_date)

    subs.save();

    messages.info(request, 'Paid Successfully!!!')

    return redirect('subscriptions')




def subscriptions(request):

    user = request.user

    subs = Subscriptions.objects.all().filter(user=request.user)

    context = {'subs': subs, 'user': user}

    return render(request, 'subscriptions.html', context)
	

def appointment_reg(request):
    user = request.user
    context = {'user': user}
    return render(request, 'Medilab/logs/appointments.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
           
                auth.login(request, user)
                print(user.is_staff)
                if user.is_staff == True:
                    
                    return redirect('home')
                else:
                    return redirect('appointment_patient')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['compname']
        name = request.POST['compname']
        compType = request.POST['compType']
        bpNo = request.POST['bpnNo']
        city = request.POST['city']
        address = request.POST['address']
        phone = request.POST['phone']
        email_address = request.POST['email_address']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email_address).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email_address, first_name=first_name, is_staff=True)
                user.save();
                client = Company.objects.create(user=user, name=name, phone=phone, compType=compType, address=address, city=city, bpNo=bpNo)
                client.save();
                messages.info(request, 'Registered Successfully')
                return redirect('login')
    else:
        return render(request, 'register.html')

def patient_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        nat_id = request.POST['nat_id']
        dob = request.POST['dob']
        city = request.POST['city']
        address = request.POST['address']
        phone = request.POST['phone']
        email_address = request.POST['email_address']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('patient_register')
            elif User.objects.filter(email=email_address).exists():
                messages.info(request, 'Email Taken')
                return redirect('patient_register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email_address, first_name=first_name, last_name=last_name, is_staff=False)
                user.save();
                client = Patient.objects.create(user=user, first_name=first_name, last_name=last_name, phone=phone, address=address, city=city, dob=dob, nat_id=nat_id, email=email_address)
                client.save();
                messages.info(request, 'Registered Successfully')
                return redirect('login')
        
    else:
        return render(request, 'patient-register.html')


def appointment(request):
    if request.method == 'POST':
        message = request.POST['message']
        date =  request.POST['date']   


        user = request.user
        book = Appointment.objects.create(message=message, date=date, user=user)
        book.save();
        user = request.user
        facility = Company.objects.get(user=user)
        appointments = Appointment.objects.all().filter(facility=facility)
        context = {'appointments': appointments, 'user': user}
        return render(request, 'appointment.html', context)

    else:

        user = request.user

        facility = Company.objects.get(user=user)

        appointments = Appointment.objects.all().filter(facility=facility)
        context = {'appointments': appointments, 'user': user}
        return render(request, 'appointment_hospital.html', context)

def appointment_patient(request):
    if request.method == 'POST':

        message = request.POST['message']

        date =  request.POST['schedule']   

        facilitie =  request.POST['facility']

        facilities = Company.objects.all()

        facility = Company.objects.get(pk=facilitie)

        user = request.user

        patient = Patient.objects.get(user=user)

        book = Appointment.objects.create(message=message, date=date, patient=patient, facility=facility)
        
        book.save();
        
        appointments = Appointment.objects.all().filter(patient=patient)
        
        context = {'appointments': appointments, 'user': user, 'facilities':facilities}
        
        return render(request, 'appointment_patient.html', context)

    else:

        user = request.user

        patient = Patient.objects.get(user=user)
        
        appointments = Appointment.objects.all().filter(patient=patient)

        facilities = Company.objects.all()

        context = {'appointments': appointments, 'user': user, 'facilities':facilities}
        
        return render(request, 'appointment_patient.html', context)


def meetTest(request, meetID):

    attempted_user = request.user

    booking = Appointment.objects.get(pk=meetID)

    context = {'booking': booking.id, 'attempted_user': attempted_user}

    return render(request, 'meeting_hosp.html', context)

def emergencyPat(request):

    attempted_user = request.user

    hospitals = Company.objects.all().filter(compType="Hospital")

    context = {'user': attempted_user, 'hospitals':hospitals}

    return render(request, 'emergency_patient.html', context)

def meetPatTest(request, meetID):
    
    attempted_user = request.user

    booking = Appointment.objects.get(pk=meetID)

    context = {'booking': booking.id, 'attempted_user': attempted_user}

    return render(request, 'meeting_pat.html', context)


def appointmentAdmin(request):
    if request.method == 'POST':
        tag = request.POST['id']

        if Appointment.objects.get_or_create(animal=tag):
            status = request.POST['status']
            book = Appointment.objects.update_or_create(animal=tag, status=status)
            book.save()

    else:
        animal = Appointment.objects.all()
        animal = {'treats': treats, 'user': user}
        return render(request, 'Medilab/logs/appointments_admin.html', context)

def sales(request):
    user = request.user
    sales = Sales.objects.all().filter(user=user)

    context = {'sales': sales, 'user': user}
    return render(request, 'sales_view.html', context)

def salesAdmin(request):
    if request.method == 'POST':
        user = request.POST['user']
        treatment = request.POST['treatment']  
        status = request.POST['status']  

        sale = Sales.objects.create(user=user, treatment=treatment, status=status)
        sale.save();

    else:
        animal = Sales.objects.all()
        animal = {'treats': treats, 'user': user}
        return render(request, 'Medilab/logs/sales_admin.html', context)



        