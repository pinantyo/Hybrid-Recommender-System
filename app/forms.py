from django import forms
from app import models

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

# Bagian Admin untuk melakukan pembuatan akun
class UserCreationForm(forms.ModelForm):
	password = forms.CharField(label='password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='password_confirm', widget=forms.PasswordInput)


	class Meta:
		model = models.AccountCustom
		fields = ('email','full_name','age','location')

	"""
		Validasi konfirmasi password
	"""
	def clean_password(self):
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')

		if password and password2 and password != password2:
			raise ValidationError('Password tidak sama')
		return password2

	"""
		Penyimpanan password
	"""
	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user

# Modifikasi akun
class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = models.AccountCustom
		fields = ('email', 'password','is_admin', 'is_active','is_staff','is_superuser')

	def clean_password(self):
		return self.initial['password']




# Bagian Tourism
class TourismCreationForm(forms.ModelForm):
	class Meta:
		model = models.TourismPlace
		fields = (
            'category','place_name','description',
            'city','price','time_minutes','lat',
            'long','img'
        )

	"""
		Penyimpanan password
	"""
	def save(self, commit=True):
		tourism = super().save(commit=False)
		if commit:
			tourism.save()
		return tourism

# Modifikasi akun
class TourismChangeForm(forms.ModelForm):
	class Meta:
		model = models.TourismPlace
		fields = (
            'category','place_name','description',
            'city','price','time_minutes','lat',
            'long','img'
        )