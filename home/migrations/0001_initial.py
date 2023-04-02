# Generated by Django 4.0.6 on 2023-02-18 06:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('book', models.CharField(default=None, max_length=200, null=True)),
                ('tag', models.AutoField(primary_key=True, serialize=False)),
                ('breed', models.CharField(max_length=200, null=True)),
                ('sex', models.CharField(max_length=200, null=True)),
                ('weight', models.FloatField()),
                ('years', models.CharField(blank=True, max_length=200, null=True)),
                ('diseases', models.CharField(blank=True, max_length=1000, null=True)),
                ('recommendations', models.CharField(blank=True, max_length=200, null=True)),
                ('referred', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.CharField(blank=True, max_length=200, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('clientType', models.CharField(default='Farmer', max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, null=True)),
                ('code', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('cost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Symptoms',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1000, null=True)),
                ('disease', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.disease')),
            ],
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('amount', models.IntegerField(default=20)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.CharField(max_length=1000, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('animal', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.animal')),
                ('treatment', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.treatment')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speciality', models.CharField(max_length=200, null=True)),
                ('clientType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.client')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctorphone', models.CharField(max_length=200, null=True)),
                ('message', models.CharField(max_length=1000, null=True)),
                ('date', models.CharField(max_length=200, null=True)),
                ('status', models.BooleanField(default=False)),
                ('animal', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.animal')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
