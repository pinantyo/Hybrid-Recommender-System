from django.conf import settings
from django.db import models
from django.utils import timezone
import os

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

import datetime, string, random
def id_randomizor():
    current_date = datetime.datetime.now()

    return ''.join(random.choices(string.ascii_lowercase,k=10))+current_date.strftime("%d%m%Y-%H%M%S-%w")




"""
    Opsi status
"""
class StatusOption(models.TextChoices):
        PROCESS = "Dalam Proses",
        FINISH = "Selesai"
"""
    Kelas untuk mengatur pembuatan akun
"""
class AuthManager(BaseUserManager):
    """
        Pembuatan Akun User (Registrasi)
    """
    def create_user(self, email, password, full_name=None, age=None, location=None, phone_number=None):
        if not email:
            raise ValueError("Kolom email tidak boleh kosong")
        if not password:
            raise ValueError("Kolom password tidak boleh kosong")

        email = self.normalize_email(email)
        user = self.model(email=email, 
                          full_name=full_name, 
                          age=age,
                          location=location,
                          phone_number=phone_number)
        
        user.set_password(password)
        user.save()
        return user

    """
        Pembuatan Akun Admin
    """
    def create_superuser(self, email, password, **other_fields):
        user = self.create_user(
                email=self.normalize_email(email),
                password=password,
            )
        user.is_admin = True
        user.is_staff=True
        user.is_superuser=True
        user.save()
        return user

"""
    Abstrak kelas untuk akun
"""
class AccountCustom(AbstractBaseUser):
    email = models.EmailField(verbose_name=_("email"),max_length=254, unique=True)
    full_name = models.CharField(max_length=300, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = AuthManager()

    def __str__(self) -> str:
        return "{}".format(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label ):
        return True


"""
    Tabel Primari
"""
class CategoryTourism(models.Model):
    category_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Category_ID')
    category_name = models.CharField(max_length=1000, unique=True, null=False)
    img = models.ImageField(upload_to='images/categories/', default='images/categories/category.jpg')

    def __str__(self) -> str:
        return "{}".format(self.category_name)


class TourismPlace(models.Model):
    place_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Tourism_ID')
    category = models.ForeignKey(CategoryTourism, on_delete=models.CASCADE, related_name="tourism_category_set")
    place_name = models.TextField()
    description = models.TextField()
    city = models.TextField()
    price = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    time_minutes = models.IntegerField(default=0)
    lat = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    long = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    img = models.ImageField(upload_to='images/',default="images/no_img.jpg")
    
    def __str__(self):
        return "{}".format(self.place_id)


"""
    Tabel Sekunder
"""
class Reservation(models.Model):
    class StatusReservation(models.TextChoices):
        PAYMENT = 'PT', _('PAYMENT')
        PAID = 'PD', _('PAID')
        ABORTED = 'AD', _('ABORTED')

    reservation_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Reservation_ID')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservation_user_set")
    place = models.ForeignKey(TourismPlace, on_delete=models.CASCADE, related_name="reservation_place_set")
    place_ratings = models.IntegerField(null=True, default=3, blank=True)
    comments = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100,choices=StatusReservation.choices,default=StatusReservation.PAYMENT)
    book_date = models.DateTimeField(null=True)
    time = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
      return "{} {} {}".format(self.user, self.place, self.place_ratings)

    def get_status(self) -> StatusReservation:
        return self.StatusReservation(self.status)


class UserPersonalization(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="personalize_user_set")
    category = models.ForeignKey(CategoryTourism, on_delete=models.CASCADE, related_name="personalization_category_set")

    def __str__(self):
      return "{}".format(self.user)


class PackageTourism(models.Model):
    package_id = models.BigAutoField(auto_created=True, primary_key=True, verbose_name='Package_ID')
    package_name = models.TextField()
    description = models.TextField()

    def __str__(self) -> str:
        return "{}".format(self.package_name)

class PackageSites(models.Model):
    package = models.ForeignKey(PackageTourism, on_delete=models.CASCADE, related_name="packages_sites_packages")
    place = models.ForeignKey(TourismPlace, on_delete=models.CASCADE, related_name="packages_sites_tourism")

    def __str__(self) -> str:
        return "{}".format(self.package)
