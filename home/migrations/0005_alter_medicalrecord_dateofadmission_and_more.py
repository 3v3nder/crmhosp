# Generated by Django 4.0.6 on 2023-03-08 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_company_medicalrecord_patient_patientspecial_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalrecord',
            name='dateOfAdmission',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='medicalrecord',
            name='dateOfDischarge',
            field=models.DateField(null=True),
        ),
    ]
