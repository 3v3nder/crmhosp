from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True,)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    dob = models.DateField()
    nat_id = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'Patient {self.nat_id}'

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    compType = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    bpNo = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'Company {self.user}'

class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=200, null=True)

    def __repr__(self):
        return f'Doctor {self.user}'

class PatientSpecial(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    bloodType = models.CharField(max_length=200, null=True)
    allergies = models.CharField(max_length=200, null=True)
    disabilities = models.CharField(max_length=200, null=True)

    def __repr__(self):
        return f'PatientSpecial {self.user}'

class MedicalRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    admitted = models.BooleanField(default=False)
    date = models.DateField(null=True, default=None)
    dateOfAdmission = models.DateField(null=True)
    discharged = models.BooleanField(default=False)
    dateOfDischarge = models.DateField(null=True)
    temp = models.CharField(max_length=200, null=True, blank=True)
    disease = models.CharField(max_length=200, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)
    bpNo = models.CharField(max_length=200, null=True, blank=True)
    prescriptions = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'MedicalRecord {self.user}'


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, default=None)
    facility = models.ForeignKey(Company, on_delete=models.CASCADE, default=None)
    message = models.CharField(max_length=1000, null=True)
    date = models.CharField(max_length=200, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'Appointment {self.user}'

class Subscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    payment_date = models.DateField()
    expiry_date = models.DateField()
    amount = models.IntegerField(default=20)

    def __str__(self):
        return f'Subscriptions {self.user}'

class Treatment(models.Model):
    name = models.CharField(max_length=200, null=True)
    cost = models.FloatField()

    def __str__(self):
        return f'Treatment {self.name}'

class Sales(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, default=None)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'Sales {self.user}-{self.treatment}'



    


