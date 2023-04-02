from django.urls import path
from home import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("appointment_reg", views.appointment_reg, name="appointment_reg"),
    path("appointment", views.appointment, name="appointment"),
    path("logout", views.logout, name="logout"),
    path("patient_register", views.patient_register, name="patient_register"),
    path("patient_home", views.patient_home, name="patient_home"),
    path("appointment_patient", views.appointment_patient, name="appointment_patient"),
    path("medical_record/", views.medical_record, name="medical_record"),
    path("medical_record_alter/", views.medical_record_alter, name="medical_record_alter"),
    path("medical_recordID/", views.medical_recordID, name="medical_recordID"),
    path("patient_record/", views.patient_record, name="patient_record"),
    path("subscriptions", views.subscriptions, name="subscriptions"),
    path("emergencyPat", views.emergencyPat, name="emergencyPat"),
    path("calling", views.calling, name="calling"),
    path("sales", views.sales, name="sales"),
    path("meetTest/<int:meetID>", views.meetTest, name="meetTest"),
    path("meetPatTest/<int:meetID>", views.meetPatTest, name="meetPatTest"),
    path("subscriptionsPay", views.subscriptionsPay, name="subscriptionsPay"),
]